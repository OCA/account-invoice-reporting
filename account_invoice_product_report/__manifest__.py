# Copyright 2026 Ecosoft Co., Ltd (https://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

{
    "name": "Account Invoice Product Report",
    "summary": "Invoice product revenue report by period, customer, and company",
    "version": "18.0.1.0.0",
    "author": "Ecosoft, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/account-invoice-reporting",
    "category": "Accounting/Accounting",
    "depends": ["account", "report_xlsx_helper"],
    "data": [
        "security/ir.model.access.csv",
        "reports/templates/invoice_product_report.xml",
        "reports/report_action.xml",
        "wizard/invoice_product_report_wizard_view.xml",
        "views/menu_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "account_invoice_product_report/static/src/js/report_action.esm.js",
            "account_invoice_product_report/static/src/xml/report.xml",
        ],
    },
    "installable": True,
    "maintainers": ["ROBBYHOOD9"],
}
