# Copyright 2025 Binhex - Adasat Torres de León
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Account Invoice Report Lot Expiration Date",
    "version": "16.0.1.0.0",
    "author": "Binhex," "Odoo Community Association (OCA)",
    "summary": "This addon adds the batch expiration date to the invoice.",
    "website": "https://github.com/OCA/account-invoice-reporting",
    "license": "AGPL-3",
    "category": "Accounting & Finance",
    "depends": [
        "sale_stock",
        "product_expiry",
    ],
    "data": ["report/report_invoice.xml"],
    "installable": True,
}
