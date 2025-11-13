# Copyright 2011 Domsense s.r.l. <http://www.domsense.com>
# Copyright 2013 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
# Copyright 2017 Tecnativa - Vicent Cubells
# Copyright 2018 Tecnativa - Pedro M. Baeza
# Copyright 2020 Tecnativa - João Marques
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from collections import defaultdict

from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    prod_lot_ids = fields.Many2many(
        comodel_name="stock.lot", compute="_compute_prod_lots", string="Production Lots"
    )

    @api.depends("move_line_ids")
    def _compute_prod_lots(self):
        for line in self:
            move_lines = line.mapped("sale_line_ids.move_ids.move_line_ids")
            delivered_lines = move_lines.filtered(lambda ml: ml.move_id.state == "done")
            delivered_qty_by_lot = defaultdict(float)
            for ml in delivered_lines:
                if ml.lot_id:
                    delivered_qty_by_lot[ml.lot_id.id] += ml.quantity
            line.prod_lot_ids = self.env["stock.lot"].browse(
                delivered_qty_by_lot.keys()
            )

    def lots_grouped_by_quantity(self):
        lot_dict = defaultdict(float)
        move_lines = self.mapped("sale_line_ids.move_ids.move_line_ids").filtered(
            lambda ml: ml.move_id.state == "done"
        )
        for ml in move_lines:
            if ml.lot_id:
                lot_dict[ml.lot_id.name] += ml.quantity
        return lot_dict
