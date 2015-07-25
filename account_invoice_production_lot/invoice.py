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

from openerp import models, fields, api


class account_invoice_line(models.Model):

    @api.one
    def _get_prod_lots(self):
        if not self.move_line_ids:
            return
        if self.move_line_ids:
            for move in self.move_line_ids:
                if move.lot_ids:
                    self.prod_lot_ids += move.lot_ids

    _inherit = "account.invoice.line"

    prod_lot_ids = fields.Many2many(
        'stock.production.lot',  'stock_prod_lot_invoice_rel', 'invoice_id',
        compute='_get_prod_lots', string="Production Lots")

    displayed_lot_id = fields.Many2one('stock.production.lot', 'Lot')
    formatted_note = fields.Html('Formatted Note')

    @api.multi
    def load_line_lots(self):
        for line in self:
            if line.prod_lot_ids:
                note = u'<ul>'
                note += u' '.join([
                    u'<li>S/N {0}</li>'.format(lot.name)
                    for lot in line.prod_lot_ids
                ])
                note += u'</ul>'
                line.write({'formatted_note': note})
        return True

    @api.model
    def create(self, vals):
        res = super(account_invoice_line, self).create(vals)
        if not vals.get('formatted_note'):
            res.load_line_lots()
        return res


class account_invoice(models.Model):

    @api.multi
    def load_lines_lots(self):
        for invoice in self:
            invoice.invoice_line.load_line_lots()
        return True

    _inherit = "account.invoice"
