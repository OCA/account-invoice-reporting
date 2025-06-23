# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Account Invoice Payment Mode Note Template",
    "summary": """
        This addon allow user to customize the payment mode note using
        jinja2 templates""",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV," "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/account-invoice-reporting",
    "depends": ["account_payment_partner", "account_payment_mode", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "wizards/account_payment_mode_note_template.xml",
        "reports/account_move.xml",
        "views/account_payment_mode.xml",
    ],
}
