# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import time
from datetime import date, datetime

from dateutil.relativedelta import relativedelta
from openerp.report import report_sxw


class Parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.list_tanggal = []
        self.localcontext.update(
            {
                "datetime": datetime,
                "date": date,
                "time": time,
                "get_tanggal": self._get_tanggal,
                "get_attendance": self._get_attendance,
                "get_overtime": self._get_overtime,
                "get_hadir": self._get_hadir,
            }
        )

    def set_context(self, objects, data, ids, report_type=None):
        self.form = data["form"]
        self.date_start = self.form["date_start"]
        self.date_end = self.form["date_end"]
        return super(Parser, self).set_context(objects, data, ids, report_type)

    def _get_tanggal(self):
        self.list_tanggal = []
        date_end = datetime.strptime(self.date_end, "%Y-%m-%d")
        cek_tanggal = datetime.strptime(self.date_start, "%Y-%m-%d")
        while cek_tanggal <= date_end:
            res = {"tanggal": cek_tanggal}
            self.list_tanggal.append(res)
            cek_tanggal = cek_tanggal + relativedelta(days=1)
        return self.list_tanggal

    def _get_attendance(self, date):
        self.list_attendance = []
        obj_attendance = self.pool.get("hr.daily_attendance")
        criteria = [
            ("date", "=", date),
        ]

        attendance_ids = obj_attendance.search(
            self.cr, self.uid, criteria, order="date asc, department_id, employee_id"
        )

        if attendance_ids:
            no = 1
            for att in obj_attendance.browse(self.cr, self.uid, attendance_ids):
                if att.state == "present":
                    ket = "Hadir"
                elif att.state == "absence":
                    ket = "Tidak Hadir"
                elif att.state == "open":
                    ket = "Cek Absen"
                res = {
                    "no": no,
                    "date": att.date,
                    "job": att.employee_id.job_id.name,
                    "employee_id": att.employee_id.id,
                    "employee": att.employee_id.name,
                    "check_in": att.real_date_start,
                    "check_out": att.real_date_end,
                    "work_hour": att.real_work_hour,
                    "state": ket,
                }
                self.list_attendance.append(res)
                no += 1
        return self.list_attendance

    def _get_overtime(self, employee, tgl):
        real_ot = 0.0
        req_ot = 0.0
        text_real_ot = "-"
        text_req_ot = "-"
        start_date = datetime.strftime(tgl, "%Y-%m-%d")
        end_date = datetime.strftime(tgl + relativedelta(days=1), "%Y-%m-%d")
        obj_ot = self.pool.get("hr.overtime_request")
        criteria = [
            ("employee_id", "=", employee),
            ("date_start", ">=", start_date),
            ("date_start", "<", end_date),
        ]
        ot_ids = obj_ot.search(self.cr, self.uid, criteria, order="employee_id")
        if ot_ids:
            for ot in obj_ot.browse(self.cr, self.uid, ot_ids):
                real_ot += ot.real_overtime_hour
                req_ot += ot.overtime_hour
            if real_ot > 0.0:
                text_real_ot = time.strftime("%H:%M", time.gmtime(real_ot * 3600))
            if req_ot > 0.0:
                text_req_ot = time.strftime("%H:%M", time.gmtime(req_ot * 3600))
        return text_req_ot + " / " + text_real_ot

    def _get_hadir(self, date, ket):
        obj_attendance = self.pool.get("hr.daily_attendance")
        criteria = [
            ("date", "=", date),
            ("state", "=", ket),
        ]
        jumlah_hadir = obj_attendance.search_count(self.cr, self.uid, criteria)
        return jumlah_hadir
