# Copyright 2017 Open Source Integrators <https://www.opensourceintegrators.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Partner Time to Pay',
    'summary': 'Add receivables and payables statistics to partners',
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Open Source Integrators, Odoo Community Association (OCA)',
    'category': 'Accounting & Finance',
    'website': 'http://www.opensourceintegrators.com',
    'depends': ['account'],
    'data': [
        'views/res_partner.xml',
    ],
    'installable': True,
}
