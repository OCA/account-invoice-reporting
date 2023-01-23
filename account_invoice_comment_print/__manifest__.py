#  Copyright 2023 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Account Invoice printed Comment",
    "summary": "Add a Comment to be printed in invoice.",
    "version": "12.0.1.0.0",
    "category": "Accounting",
    "author": "TAKOBI, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/account-invoice-reporting"
               "/tree/12.0/account_invoice_comment_print",
    "license": "AGPL-3",
    "depends": [
        "account",
    ],
    "data": [
        "views/account_invoice_views.xml",
        "views/res_partner_views.xml",
        "templates/account_invoice_templates.xml",
    ],
}
