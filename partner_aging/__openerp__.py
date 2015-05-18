# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 Ursa Informative Systems (<www.ursainfosystems.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

{
    "name": "Interactive Partner Aging",
    "version": "1.7.2",
    "author": 'Ursa Information Systems',
    "summary": "Aging as a view - invoices and credits (Ursa)",
    'maintainer': 'Ursa Information Systems',
    'website': 'http://www.ursainfosystems.com',
    "category": 'Accounting & Finance',
    "images": [],
    "depends": ["base", "account_accountant"],
    "data": [
        'partner_aging_supplier.xml',
        'partner_aging_customer.xml',
        'security/ir.model.access.csv',
    ],
    "test": [
    ],
    "auto_install": False,
    "application": False,
    "installable": True,
}
