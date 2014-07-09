# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module Copyright (C) 2014 Therp BV (<http://therp.nl>).
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
'''Extend model stock.picking'''
from openerp.osv import orm


class StockPicking(orm.Model):
    '''Modify stock picking to fill delivery address'''
    _inherit = 'stock.picking'

    def _prepare_invoice(self, cr, uid, picking, partner,
                         inv_type, journal_id, context=None):
        """\
Inherit the original function of the 'stock' module in order to fill delivery
address when present in sales order.
"""
        invoice_vals = super(StockPicking, self)._prepare_invoice(
            cr, uid, picking, partner, inv_type, journal_id, context=context)
        if picking.sale_id and picking.sale_id.partner_shipping_id:
            invoice_vals['partner_shipping_id'] = (
                picking.sale_id.partner_shipping_id.id)
        return invoice_vals
