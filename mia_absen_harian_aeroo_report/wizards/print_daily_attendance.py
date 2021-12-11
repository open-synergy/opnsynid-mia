# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime

from openerp import api, fields, models
from openerp.exceptions import Warning as UserError
from openerp.tools.translate import _


class PrintDailyAttendance(models.TransientModel):
    _name = "hr.print_daily_attendance"
    _description = "Print Daily Attendance"

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
        selection=[
            ("ods", "ODS"),
        ],
        default="ods",
    )
    # ('ods', 'ODS'),
    # ('xls', 'XLS'),
    # ('pdf', 'PDF'),

    @api.constrains("date_start", "date_end")
    def _check_date(self):
        strWarning = _("Date start must be greater than date end")
        if self.date_start and self.date_end:
            if self.date_start > self.date_end:
                raise UserError(strWarning)

    @api.multi
    def action_print(self):
        self.ensure_one()

        datas = {}
        output_format = ""

        datas["form"] = self.read()[0]

        if self.output_format == "xls":
            output_format = "daily_attendance_xls"
        elif self.output_format == "ods":
            output_format = "daily_attendance_ods"
        elif self.output_format == "pdf":
            output_format = "daily_attendance_pdf"

        return {
            "type": "ir.actions.report.xml",
            "report_name": output_format,
            "datas": datas,
        }
