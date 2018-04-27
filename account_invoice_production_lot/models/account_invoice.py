# -*- coding: utf-8 -*-
# Copyright 2011 Domsense s.r.l. <http://www.domsense.com>
# Copyright 2013 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
# Copyright 2017 Vicent Cubells <vicent.cubells@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools.misc import formatLang


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    order_line_ids = fields.Many2many(
        comodel_name='sale.order.line',
        relation='sale_order_line_invoice_rel',
        column1='invoice_line_id',
        column2='order_line_id',
        string='Order Lines',
        readonly=True,
    )

    prod_lot_ids = fields.Many2many(
        comodel_name='stock.production.lot',
        compute='_compute_prod_lots',
        string="Production Lots",
    )

    lot_formatted_note = fields.Html(
        string='Formatted Note',
        compute='_compute_line_lots',
    )

    @api.multi
    def _compute_prod_lots(self):
        for line in self:
            line.prod_lot_ids = line.move_line_ids.mapped('lot_ids')

    @api.multi
    def _compute_line_lots(self):
        for line in self:
            if line.prod_lot_ids:
                res = line.quantity_by_lot()
                note = u'<ul>'
                lot_strings = []
                for lot in line.prod_lot_ids:
                    lot_string = u'<li>S/N %s%s</li>' % (
                        lot.name, u' (%s)' % res[lot] if res.get(lot) else '')
                    lot_strings.append(lot_string)
                note += u' '.join(lot_strings)
                note += u'</ul>'
                line.lot_formatted_note = note

    def quantity_by_lot(self):
        self.ensure_one()
        move_ids = self.move_line_ids
        res = {}
        for move in move_ids:
            for quant in move.quant_ids:
                if (
                    quant.lot_id and
                    quant.location_id.id == move.location_dest_id.id
                ):
                    if quant.lot_id not in res:
                        res[quant.lot_id] = quant.qty
                    else:
                        res[quant.lot_id] += quant.qty
        for lot in res:
            if lot.product_id.tracking == 'lot':
                res[lot] = formatLang(self.env, res[lot])
            else:
                # If not tracking By lots or not By Unique Serial Number,
                # quantity is not relevant
                res[lot] = False
        return res
