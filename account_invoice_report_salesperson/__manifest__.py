# Copyright 2024 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

{
    "name": "Account Invoice Report Salesperson",
    "summary": "Salesperson info in Invoice report",
    "version": "16.0.1.0.1",
    "development_status": "Alpha",
    "category": "Account",
    "website": "https://github.com/OCA/account-invoice-reporting",
    "author": "Moduon, Odoo Community Association (OCA)",
    "maintainers": ["Shide"],
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "account",
    ],
    "data": [
        "views/report_invoice.xml",
    ],
}
