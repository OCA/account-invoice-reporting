# Copyright 2026 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
{
    "name": "Account Invoice Report Without Taxation",
    "summary": """
        Hides line taxes data in account invoice report
    """,
    "author": "Solvos, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "version": "18.0.1.0.0",
    "category": "Accounting & Finance",
    "website": "https://github.com/OCA/account-invoice-reporting",
    "depends": ["account"],
    "data": [
        "reports/account_invoice_template.xml",
        "views/res_config_settings_views.xml",
    ],
    "installable": True,
}
