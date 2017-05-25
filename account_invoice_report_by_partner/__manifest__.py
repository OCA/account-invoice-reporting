# -*- coding: utf-8 -*-
# Copyright 2014 Angel Moya <angel.moya@domatix.com>
# Copyright 2017 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "Invoice Report by Partner",
    'version': "10.0.1.0.0",
    'author': "Domatix, "
              "Tecnativa, "
              "Odoo Community Association (OCA)",
    'website': 'http://www.domatix.com/',
    'category': 'Accounting & Finance',
    'license': "AGPL-3",
    'depends': [
        'account',
    ],
    'data': [
        'views/partner_view.xml',
    ],
    'installable': True,
}
