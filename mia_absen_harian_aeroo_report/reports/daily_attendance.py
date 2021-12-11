# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models, tools


class DailyAttendance(models.Model):
    _name = "hr.daily_attendance"
    _description = "Daily Attendance"
    _auto = False

    date = fields.Date(
        string="Date",
    )
    date_start = fields.Datetime(
        string="Date Start",
    )
    date_end = fields.Datetime(
        string="Date End",
    )
    real_date_start = fields.Datetime(
        string="Real Date Start",
    )
    real_date_end = fields.Datetime(
        string="Real Date End",
    )
    employee_id = fields.Many2one(
        string="Employee",
        comodel_name="hr.employee",
    )
    department_id = fields.Many2one(
        string="Department",
        comodel_name="hr.department",
    )
    schedule_work_hour = fields.Float(
        string="Schedule Work Hours",
    )
    real_work_hour = fields.Float(
        string="Real Work Hours",
    )
    early_start_hour = fields.Float(
        string="Early Start Hours",
    )
    late_start_hour = fields.Float(
        string="Late Start Hours",
    )
    finish_early_hour = fields.Float(
        string="Finish Early Hours",
    )
    finish_late_hour = fields.Float(
        string="Finish Late Hours",
    )
    sheet_id = fields.Many2one(
        string="Timesheet",
        comodel_name="hr_timesheet_sheet.sheet",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("absence", "Absence"),
            ("open", "Open"),
            ("present", "Present"),
        ],
    )

    def _select(self):
        select_str = """
        SELECT
            row_number() OVER() as id,
            CAST(a.date_start AS date) AS date,
            a.date_start AS date_start,
            a.date_end AS date_end,
            c.name AS real_date_start,
            d.name AS real_date_end,
            a.employee_id AS employee_id,
            b.department_id AS department_id,
            a.schedule_work_hour AS schedule_work_hour,
            a.real_work_hour AS real_work_hour,
            a.early_start_hour AS early_start_hour,
            a.late_start_hour AS late_start_hour,
            a.finish_early_hour AS finish_early_hour,
            a.finish_late_hour AS finish_late_hour,
            a.sheet_id AS sheet_id,
            a.state AS state
        """
        return select_str

    def _from(self):
        from_str = """
        hr_timesheet_attendance_schedule AS a
        """
        return from_str

    def _where(self):
        where_str = """
        WHERE 1 = 1
        """
        return where_str

    def _join(self):
        join_str = """
        JOIN hr_employee AS b ON
            a.employee_id = b.id
        LEFT JOIN hr_attendance c ON
            a.start_attendance_id = c.id
        LEFT JOIN hr_attendance d ON
            a.end_attendance_id = d.id
        """
        return join_str

    def _group_by(self):
        group_str = """
        GROUP BY
            a.date_start,
            a.date_end,
            c.name,
            d.name,
            a.employee_id,
            b.department_id,
            a.schedule_work_hour,
            a.real_work_hour,
            a.early_start_hour,
            a.late_start_hour,
            a.finish_early_hour,
            a.finish_late_hour,
            a.sheet_id,
            a.state
        """
        return group_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        # pylint: disable=locally-disabled, sql-injection
        cr.execute(
            """CREATE or REPLACE VIEW %s as (
            %s
            FROM %s
            %s
            %s
            %s
        )"""
            % (
                self._table,
                self._select(),
                self._from(),
                self._join(),
                self._where(),
                self._group_by(),
            )
        )
