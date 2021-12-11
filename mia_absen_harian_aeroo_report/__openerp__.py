# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Daily Attendance Aeroo Report",
    "version": "8.0.1.0.0",
    "category": "Human Resource",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "report_aeroo",
        "hr_timesheet_attendance_schedule",
        "hr_timesheet_computation_overtime",
    ],
    "data": [
        "security/ir.model.access.csv",
        "reports/daily_attendance_reports.xml",
        "wizards/print_daily_attendance_views.xml",
    ],
}
