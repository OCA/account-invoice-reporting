# Copyright 2011 Domsense s.r.l. <http://www.domsense.com>
# Copyright 2013 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
# Copyright 2017 Vicent Cubells <vicent.cubells@tecnativa.com>
# Copyright 2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

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
            line.prod_lot_ids = line.mapped(
                'move_line_ids.move_line_ids.lot_id'
            )

    @api.multi
    def _compute_line_lots(self):
        for line in self:
            note = '<ul>'
            lot_strings = []
            for sml in line.mapped('move_line_ids.move_line_ids'):
                if sml.lot_id:
                    if sml.product_id.tracking == 'serial':
                        lot_strings.append('<li>%s %s</li>' % (
                            _('S/N'), sml.lot_id.name,
                        ))
                    else:
                        lot_strings.append('<li>%s %s (%s)</li>' % (
                            _('Lot'), sml.lot_id.name, sml.qty_done,
                        ))
            if lot_strings:
                note += ' '.join(lot_strings)
                note += '</ul>'
                line.lot_formatted_note = note
