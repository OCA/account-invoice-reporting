# -*- coding: utf-8 -*-
# Copyright 2011 Domsense s.r.l. <http://www.domsense.com>
# Copyright 2013 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
# Copyright 2017 Vicent Cubells <vicent.cubells@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime


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
            if not line.order_line_ids:
                return
            line.prod_lot_ids = self.mapped(
                'order_line_ids.procurement_ids.move_ids.lot_ids')

    @api.multi
    def _compute_line_lots(self):
        lang = self.env['res.lang']._lang_get(self.env.lang)
        date_format = lang.date_format
        for line in self:
            if line.prod_lot_ids:
                note = u'<ul>'
                date = ""
                for lot in line.prod_lot_ids:
                    if line.invoice_id.company_id.lot_use_date:
                        if lot.use_date:
                            date = datetime.strptime(
                                lot.use_date,
                                DEFAULT_SERVER_DATETIME_FORMAT).strftime(
                                date_format)
                        note += u'<li>S/N' + unicode(
                            lot.name) + ' - ' + unicode(date) + '</li>'
                    else:
                        note += u'<li>S/N ' + unicode(lot.name) + '</li>'
                note += u'</ul>'
                line.lot_formatted_note = note
