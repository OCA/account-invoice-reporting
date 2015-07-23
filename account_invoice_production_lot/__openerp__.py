# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Author: Lorenzo Battistini <lorenzo.battistini@agilebg.com>
#    Copyright (C) 2011 Domsense s.r.l. (<http://www.domsense.com>).
#    Copyright (C) 2013 Agile Business Group  (<http://www.agilebg.com>)
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
    "version": "8.0.1.1.0",
    'category': 'Generic Modules/Accounting',
    "depends": [
        "account_accountant",
        "sale_stock",
        "stock_picking_invoice_link",
        ],
    "author": "Agile Business Group,Odoo Community Association (OCA)",
    "summary": "Display delivered serial numbers in invoice",
    'website': 'http://www.agilebg.com',
    'license': 'AGPL-3',
    'data': [
        'invoice_view.xml',
        'view/report_invoice.xml',
        ],
    'demo': [
        'demo/sale.yml',
        ],
    'installable': True,
    'active': False,
}
