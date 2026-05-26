# Copyright 2026 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)
{
    "name": "Account Invoice Report Lot Expiry Date",
    "summary": "Display expiry date in the lots table of the invoice report",
    "version": "18.0.1.0.1",
    "development_status": "Alpha",
    "category": "Accounting/Accounting",
    "website": "https://github.com/OCA/account-invoice-reporting",
    "author": "Moduon, Odoo Community Association (OCA)",
    "maintainers": ["chienandalu", "rafaelbn"],
    "license": "AGPL-3",
    "depends": [
        "stock_account",
        "product_expiry",
    ],
    "data": [
        "views/report_invoice.xml",
    ],
}
