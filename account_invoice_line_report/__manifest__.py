# Copyright 2017 Carlos Dauden - Tecnativa <carlos.dauden@tecnativa.com>
# Copyright 2018 Vicent Cubells - Tecnativa <vicent.cubells@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Account Invoice Line Report',
    'summary': 'New view to manage invoice lines information',
    'version': '11.0.1.0.0',
    'category': 'Account',
    'website': 'http://www.tecnativa.com',
    'author': 'Tecnativa, '
              'Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'depends': [
        'account',
    ],
    'data': [
        'report/account_invoice_report_view.xml',
    ],
    'installable': True,
}
