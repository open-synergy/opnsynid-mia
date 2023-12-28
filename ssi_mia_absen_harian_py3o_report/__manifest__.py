# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Daily Attendance py3o Report",
    "version": "14.0.1.0.0",
    "category": "Human Resource",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "report_py3o",
        "ssi_timesheet_attendance",
        "ssi_hr_overtime",
    ],
    "external_dependencies": {
        "python": [
            "py3o.template",
            "py3o.formats",
        ],
        "deb": ["libreoffice"],
    },
    "data": [
        "security/ir.model.access.csv",
        "reports/daily_attendance_reports.xml",
        "wizards/print_daily_attendance_views.xml",
    ],
}
