# -*- coding: utf-8 -*-
# Copyright 2019 PlanetaTIC - Marc Poch <mpoch@planetatic.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Account Invoice Report With Taxes",
    "version": "10.0.1.0.0",
    'description': 'shows prices with taxes on account invoice report',
    "author": "PlanetaTIC",
    "website": "https://www.planetatic.com",
    "license": "AGPL-3",
    "category": "Accounting",
    'depends': [
        'account',
    ],
    "data": [
        'report/account_invoice_report_view.xml',
    ],
    "qweb": [],
    "installable": True,
}
