# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Author: Lorenzo Battistini <lorenzo.battistini@agilebg.com>
#    Copyright (C) 2011 Domsense s.r.l. (<http://www.domsense.com>).
#    Copyright (C) 2013 Agile Business Group sagl (<http://www.agilebg.com>)
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
##############################################################################


{
    "name": "Invoice Production Lots",
    "version": "1.1",
    'category': 'Generic Modules/Accounting',
    "depends": [
        "sale_stock",
        "invoice_webkit",
        ],
    "author": "Agile Business Group",
    "summary": "Display delivered serial numbers in invoice",
    "description": """
This module prints, for each (customer) invoice line, the delivered production
lots. The serial numbers are displayed in the "formatted note" field,
introduced by invoice_webkit module""",
    'website': 'http://www.agilebg.com',
    'data': [
        'invoice_view.xml',
        ],
    'demo': [],
    'test': [
        'test/sale.yml',
        ],
    'installable': True,
    'active': False,
}
