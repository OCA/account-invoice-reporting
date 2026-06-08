# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Account Invoice Report Untaxed Unrounded",
    "summary": "Show unrounded line subtotals and untaxed amounts on the invoice "
    "report when currency rounding hides decimals",
    "version": "18.0.1.0.0",
    "category": "Account",
    "website": "https://github.com/OCA/account-invoice-reporting",
    "author": "Quartile, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["account"],
    "data": [
        "views/res_config_settings_views.xml",
        "views/report_invoice.xml",
    ],
    "maintainers": ["yostashiro", "aungkokolin1997"],
    "installable": True,
}
