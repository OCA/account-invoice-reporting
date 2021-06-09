# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    has_order_position = fields.Boolean(compute="_compute_has_order_position")

    @api.depends("invoice_line_ids.position_formatted")
    def _compute_has_order_position(self):
        for record in self:
            record.has_order_position = any(
                record.invoice_line_ids.mapped("position_formatted")
            )


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    position_formatted = fields.Char(compute="_compute_position_formatted")

    @api.depends("sale_line_ids.position")
    def _compute_position_formatted(self):
        for record in self:
            if record.display_type:
                record.position_formatted = ""
                continue
            values = [
                val for val in record.sale_line_ids.mapped("position_formatted") if val
            ]
            record.position_formatted = "/".join(values)
