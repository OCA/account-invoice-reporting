# Copyright (C) 2019 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Hide invoice lines from the PDF report if the unit price is 0',
    'version': '12.0.1.0.0',
    'category': 'Accounting',
    'author': 'Open Source Integrators, '
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/account-invoice-reporting',
    'depends': [
        'account',
    ],
    'data': [
        'views/account_invoice_view.xml',
        'views/report_invoice.xml',
    ],
    'installable': True,
    'license': 'AGPL-3',
    'development_status': 'Beta',
    'maintainers': [
        'bodedra',
        'max3903',
    ],
}
