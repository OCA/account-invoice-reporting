# Copyright 2020 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Account Invoice Report Payment Extended Info",
    "summary": "Show payment extended info in invoice",
    "version": "13.0.1.0.1",
    "category": "Accounting",
    "website": "https://github.com/OCA/account-invoice-reporting",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["account"],
    "data": ["data/payment_info_data.xml", "views/report_invoice.xml"],
}
