# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Account Invoice Line Report',
    'summary': 'New views to manage invoice lines information',
    'version': '10.0.1.0.0',
    'category': 'Account',
    'author': 'Tecnativa, '
              'Komit Consulting, '
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/account-invoice-reporting',
    'license': 'AGPL-3',
    'depends': [
        'account',
    ],
    'data': [
        'report/account_invoice_report_view.xml',
    ],
    'installable': True,
}
