# Copyright 2026 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

{
    "name": "Account Invoice Report Stock Packaging",
    "summary": "Display Packaging on Invoice Report",
    "version": "18.0.1.0.1",
    "development_status": "Alpha",
    "category": "Accounting",
    "website": "https://github.com/OCA/account-invoice-reporting",
    "author": "Moduon, Odoo Community Association (OCA)",
    "maintainers": ["Shide", "rafaelbn"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "stock_move_packaging_qty",
        "stock_picking_invoice_link",
    ],
    "data": [
        "views/report_invoice.xml",
    ],
}
