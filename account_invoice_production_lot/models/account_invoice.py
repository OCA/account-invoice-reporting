# -*- coding: utf-8 -*-
# Copyright 2011 Domsense s.r.l. <http://www.domsense.com>
# Copyright 2013 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
# Copyright 2017 Vicent Cubells <vicent.cubells@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


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
        relation='stock_prod_lot_invoice_rel',
        column1='invoice_id',
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
            if not line.order_line_ids:
                return
            line.prod_lot_ids = self.mapped(
                'order_line_ids.procurement_ids.move_ids.lot_ids')

    @api.multi
    def _compute_line_lots(self):
        for line in self:
            if line.prod_lot_ids:
                note = u'<ul>'
                note += u' '.join([
                    u'<li>S/N {0}</li>'.format(lot.name)
                    for lot in line.prod_lot_ids
                ])
                note += u'</ul>'
                line.lot_formatted_note = note
