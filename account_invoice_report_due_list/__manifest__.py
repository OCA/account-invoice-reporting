# Copyright 2018 Tecnativa - Carlos Dauden
# Copyright 2020 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Account Invoice Report Due List",
    "summary": "Show multiple due data in invoice",
    "version": "13.0.1.1.0",
    "category": "Accounting",
    "website": "https://github.com/OCA/account-invoice-reporting",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["account"],
    "data": ["views/account_invoice_view.xml", "views/report_invoice.xml"],
}
