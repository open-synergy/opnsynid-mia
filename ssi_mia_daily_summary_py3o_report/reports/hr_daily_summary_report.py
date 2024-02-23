# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class HrDailySummaryReport(models.Model):
    _name = "hr.daily_summary_report"
    _description = "Daily Summary Report"
    _auto = False

    date = fields.Date(
        string="Date",
    )
    job_id = fields.Many2one(
        string="Job Position",
        comodel_name="hr.job",
    )
    employee_id = fields.Many2one(
        string="Employee",
        comodel_name="hr.employee",
    )
    daily_summary_id = fields.Many2one(
        string="Daily Summary",
        comodel_name="hr.timesheet_daily_summary",
    )
    sheet_id = fields.Many2one(
        string="Timesheet",
        comodel_name="hr.timesheet",
    )
    attendance_id = fields.Many2one(
        string="Attendance",
        comodel_name="hr.timesheet_attendance",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("present", "Present"),
            ("open", "Open"),
            ("absence", "Absence"),
        ])


    @property
    def _table_query(self):
        return "%s %s %s %s %s" % (
            self._select(),
            self._from(),
            self._join(),
            self._where(),
            self._group_by(),
        )

    @api.model
    def _select(self):
        select_str = """
        SELECT
            row_number() OVER() as id,
            ds.date AS date,
            e.job_id AS job_id,
            ts.employee_id AS employee_id,
            ds.id AS daily_summary_id,
            ds.sheet_id AS sheet_id,
            a.id AS attendance_id,
            CASE
                WHEN a.state IS NOT NULL THEN a.state
                ELSE 'absence'
            END AS state
        """
        return select_str

    @api.model
    def _from(self):
        from_str = """
        FROM hr_timesheet_daily_summary AS ds
        """
        return from_str

    @api.model
    def _where(self):
        where_str = """
        WHERE 1 = 1
        """
        return where_str

    @api.model
    def _join(self):
        join_str = """
        LEFT JOIN
            hr_timesheet AS ts ON ts.id = ds.sheet_id
        LEFT JOIN
            hr_employee AS e ON e.id = ts.employee_id
        LEFT JOIN
            hr_timesheet_attendance AS a ON a.sheet_id = ds.sheet_id AND a.date = ds.date
        """
        return join_str

    @api.model
    def _group_by(self):
        group_str = """
        GROUP BY
            ds.date,
            e.job_id,
            ts.employee_id,
            ds.id,
            ds.sheet_id,
            a.id,
            a.state
        """
        return group_str
