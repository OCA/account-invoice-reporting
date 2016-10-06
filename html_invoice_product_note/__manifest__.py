# -*- coding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2013 Camptocamp SA (http://www.camptocamp.com)
#   @author Nicolas Bessi
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

{'name': 'HTML note in product reported in invoice report',
 'version': '1.0.0',
 'category': 'other',
 'description': """
Sale product note
=================

This module replaces the invoice description field of product.product
with a HTML field.

It takes care of adding this description into the HTML `note` field
of the invoice line when the product is set.""",
 'author': "Camptocamp,Odoo Community Association (OCA)",
 'website': 'http://www.camptocamp.com',
 'license': 'AGPL-3',
 'depends': ['product', 'account', 'invoice_webkit'],
 'data': [],
 'test': [],
 'installable': False,
 'active': False,
 }
