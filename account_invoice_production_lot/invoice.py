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


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    prod_lot_ids = fields.Many2many(
        'stock.production.lot',  'stock_prod_lot_invoice_rel', 'invoice_id',
        compute='_get_prod_lots', string="Production Lots")

    lot_formatted_note = fields.Html(
        'Formatted Note', compute='load_line_lots')

    @api.multi
    @api.depends("sale_line_ids")
    def _get_prod_lots(self):
        for invoice_line in self:
            if invoice_line.sale_line_ids:
                invoice_line.prod_lot_ids = invoice_line.mapped(
                    'sale_line_ids.procurement_ids.move_ids.lot_ids')

    @api.multi
    @api.depends("prod_lot_ids")
    def load_line_lots(self):
        for invoice_line in self:
            if invoice_line.prod_lot_ids:
                note = u'<ul>'
                note += u' '.join([
                    u'<li>S/N {0}</li>'.format(lot.name)
                    for lot in invoice_line.prod_lot_ids
                ])
                note += u'</ul>'
                invoice_line.lot_formatted_note = note
