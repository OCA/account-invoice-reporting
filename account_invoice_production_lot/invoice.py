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

from openerp.osv import fields, orm


class account_invoice_line(orm.Model):

    def _get_prod_lots(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        for line in self.browse(cr, uid, ids, context=context):
            result[line.id] = []
            if line.move_line_ids:
                for move in line.move_line_ids:
                    if move.prodlot_id:
                        result[line.id].append(move.prodlot_id.id)
            else:
                for order_line in line.order_lines:
                    for move in order_line.move_ids:
                        if move.prodlot_id:
                            result[line.id].append(move.prodlot_id.id)
        return result

    _inherit = "account.invoice.line"

    _columns = {
        # order_lines is the reverse of invoice_lines field of sale module
        'order_lines': fields.many2many(
            'sale.order.line', 'sale_order_line_invoice_rel', 'invoice_id',
            'order_line_id', 'Order Lines', readonly=True),
        'prod_lot_ids': fields.function(
            _get_prod_lots, method=True, type='many2many',
            relation="stock.production.lot", string="Production Lots"),
        'displayed_lot_id': fields.many2one('stock.production.lot', 'Lot'),
        }

    def load_line_lots(self, cr, uid, ids, context=None):
        for line in self.browse(cr, uid, ids, context):
            if line.prod_lot_ids:
                note = u'<ul> '
                note += u' '.join([
                    u'<li>S/N {0}</li>'.format(lot.name)
                    for lot in line.prod_lot_ids
                ])
                note += u' </ul>'
                line.write({'formatted_note': note}, context=context)
        return True

    def create(self, cr, uid, vals, context=None):
        res = super(account_invoice_line, self).create(cr, uid, vals, context)
        if not vals.get('formatted_note'):
            self.load_line_lots(cr, uid, [res], context)
        return res

class account_invoice(orm.Model):

    def load_lines_lots(self, cr, uid, ids, context=None):
        invoices = self.browse(cr, uid, ids, context)
        inv_line_obj = self.pool.get('account.invoice.line')
        for invoice in invoices:
            inv_line_obj.load_line_lots(cr, uid, [l.id for l in invoice.invoice_line], context)
        return True

    _inherit = "account.invoice"
