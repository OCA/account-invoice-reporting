# Copyright (C) 2019 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Partner Time to Pay",
    "summary": "Add receivables and payables statistics to partners",
    "version": "15.0.1.2.0",
    "license": "AGPL-3",
    "development_status": "Beta",
    "author": "Open Source Integrators, Odoo Community Association (OCA), Moduon",
    "category": "Accounting & Finance",
    "website": "https://github.com/OCA/account-invoice-reporting",
    "maintainers": ["max3903", "rafaelbn", "Shide"],
    "depends": ["account"],
    "data": [
        "views/account_move_view.xml",
        "views/res_partner_view.xml",
    ],
    "installable": True,
}
