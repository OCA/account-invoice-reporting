# -*- coding: utf-8 -*-
# Copyright 2017 Ursa Information Systems <http://www.ursainfosystems.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Partner Days to Pay',
    'summary': 'Adds receivables and payables statistics to partners',
    'version': '10.0.1.0.1',
    'license': 'AGPL-3',
    'author': 'Ursa Information Systems, Odoo Community Association (OCA)',
    'category': 'Accounting & Finance',
    'website': 'http://www.ursainfosystems.com',
    'depends': ['account'],
    'data': [
        'views/res_partner.xml',
    ],
    'installable': True,
}
