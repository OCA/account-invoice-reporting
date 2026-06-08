# Copyright 2026 Quartile (https://www.quartile.co)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
{
    "name": "Account Invoice Report Untaxed Unrounded",
    "summary": "Show unrounded line subtotals in the invoice report when "
    "currency rounding hides decimals",
    "version": "18.0.1.0.0",
    "category": "Account",
    "website": "https://github.com/OCA/account-invoice-reporting",
    "author": "Quartile, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "development_status": "Alpha",
    "application": False,
    "installable": True,
    "depends": ["account"],
    "data": [
        "views/report_invoice.xml",
    ],
}
