# Copyright 2020 Lorenzo Battistini @ TAKOBI
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Invoice Packages",
    "version": "12.0.1.0.0",
    "author": "TAKOBI, "
              "Odoo Community Association (OCA)",
    "summary": "Display delivered packages in invoice",
    'website': 'https://github.com/OCA/account-invoice-reporting',
    'license': 'AGPL-3',
    'category': 'Accounting & Finance',
    "depends": [
        "account",
        "stock_picking_invoice_link",
    ],
    'data': [
        "views/account_invoice_views.xml",
        "report/report_invoice.xml",
    ],
    'installable': True,
}
