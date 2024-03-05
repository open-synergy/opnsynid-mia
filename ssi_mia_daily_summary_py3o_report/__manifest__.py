# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Daily Summary py3o Report",
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
        "reports/hr_daily_summary_reports.xml",
        "wizards/hr_print_daily_summary_views.xml",
    ],
}
