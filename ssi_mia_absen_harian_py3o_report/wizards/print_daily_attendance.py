# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging
from datetime import datetime

import pytz
from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

try:
    from py3o.formats import Formats
except ImportError:
    _logger.warning("Cannot import py3o.formats")


class PrintDailyAttendance(models.TransientModel):
    _name = "hr.print_daily_attendance"
    _description = "Print Daily Attendance"

    @api.model
    def _get_py3o_filetypes(self):
        formats = Formats()
        names = formats.get_known_format_names()
        selections = []
        for name in names:
            if name in ["doc", "docx", "docbook", "html"]:
                continue
            description = name
            if formats.get_format(name).native:
                description = description + " " + _("(Native)")
            selections.append((name, description))
        return selections

    date_start = fields.Date(
        string="Date Start",
        default=datetime.now().strftime("%Y-%m-%d"),
        required=True,
    )
    date_end = fields.Date(
        string="Date End",
        default=datetime.now().strftime("%Y-%m-%d"),
        required=True,
    )
    output_format = fields.Selection(
        string="Output Format",
        required=True,
        selection="_get_py3o_filetypes",
        default="xls",
    )

    @api.constrains("date_start", "date_end")
    def _check_date(self):
        str_warning = _("Date start must be greater than date end")
        for rec in self:
            if rec.date_start and rec.date_end:
                if rec.date_start > rec.date_end:
                    raise ValidationError(str_warning)

    def _get_attendance(self, date):
        list_attendance = []
        dt_start = datetime(date.year, date.month, date.day, 0, 0, 1)
        convert_dt_start = dt_start.strftime("%Y-%m-%d %H:%M:%S")
        dt_end = datetime(date.year, date.month, date.day, 23, 23, 59)
        convert_dt_end = dt_end.strftime("%Y-%m-%d %H:%M:%S")
        start_utc = self._convert_datetime_utc(convert_dt_start)
        end_utc = self._convert_datetime_utc(convert_dt_end)
        obj_attendance = self.env["hr.daily_attendance"]
        criteria = [
            ("date_start", ">=", start_utc),
            ("date_start", "<=", end_utc),
        ]

        attendance_ids = obj_attendance.search(
            criteria, order="date asc, department_id, employee_id"
        )
        if attendance_ids:
            no = 1
            for att in attendance_ids:
                if att.state == "present":
                    status = "Hadir"
                elif att.state == "absence":
                    status = "Tidak Hadir"
                else:
                    status = "Cek Absen"
                res = {
                    "no": no,
                    "date": att.date,
                    "job": att.employee_id.job_id.name,
                    "employee_id": att.employee_id.id,
                    "employee": att.employee_id.name,
                    "check_in": self.get_tz_datetime(utc_datetime=att.real_date_start),
                    "check_out": self.get_tz_datetime(utc_datetime=att.real_date_end),
                    "work_hour": "{:02.0f}:{:02.0f}".format(
                        *divmod(att.real_work_hour * 60, 60)
                    ),
                    "state": status,
                }
                list_attendance.append(res)
                no += 1
        return list_attendance

    def _get_overtime(self, employee_id, current_date):
        real_ot = 0.0
        req_ot = 0.0
        text_real_ot = "-"
        text_req_ot = "-"
        start_date = datetime.strftime(current_date, "%Y-%m-%d")
        end_date = datetime.strftime(current_date + relativedelta(days=1), "%Y-%m-%d")
        obj_ot = self.env["hr.overtime"]
        criteria = [
            ("employee_id", "=", employee_id),
            ("date_start", ">=", start_date),
            ("date_start", "<", end_date),
        ]
        ot_ids = obj_ot.search(criteria, order="employee_id")
        if ot_ids:
            for ot in ot_ids:
                real_ot += ot.realized_hour
                req_ot += ot.planned_hour
            if real_ot > 0.0:
                text_real_ot = "{:02.0f}:{:02.0f}".format(*divmod(real_ot * 60, 60))
            if req_ot > 0.0:
                text_req_ot = "{:02.0f}:{:02.0f}".format(*divmod(req_ot * 60, 60))
        return f"{text_req_ot} / {text_real_ot}"

    def _get_status_count(self, date, status):
        obj_attendance = self.env["hr.daily_attendance"]
        criteria = [
            ("date", "=", date),
            ("state", "=", status),
        ]
        jumlah_hadir = obj_attendance.search_count(criteria)
        return jumlah_hadir

    def _get_present(self, date):
        return self._get_status_count(date=date, status="present")

    def _get_absence(self, date):
        return self._get_status_count(date=date, status="absence")

    def _get_open(self, date):
        return self._get_status_count(date=date, status="open")

    def get_tz_datetime(self, utc_datetime=False, tz=False):
        if not utc_datetime:
            return "-"
        if not tz:
            tz = self.env.user.tz or "Asia/Jakarta"
        tz_datetime = pytz.UTC.localize(utc_datetime).astimezone(pytz.timezone(tz))
        return tz_datetime.strftime("%Y-%m-%d %H:%M:%S")

    def _convert_datetime_utc(self, dt):
        if dt:
            user = self.env.user
            convert_dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
            if user.tz:
                tz = pytz.timezone(user.tz)
            else:
                tz = pytz.utc
            convert_utc = tz.localize(convert_dt).astimezone(pytz.utc)
            format_utc = convert_utc.strftime("%Y-%m-%d %H:%M:%S")
            return format_utc
        else:
            return "-"

    def get_date_ranges(self):
        date_ranges = []
        date_start = self.date_start
        while date_start <= self.date_end:
            date_ranges.append(date_start)
            date_start = date_start + relativedelta(days=1)
        return date_ranges

    def action_print(self):
        self.ensure_one()
        report_id = self.env.ref(
            "ssi_mia_absen_harian_py3o_report.daily_attendance_report_py3o"
        )
        report_id.sudo().write({"py3o_filetype": self.output_format})
        return report_id.report_action(self)
