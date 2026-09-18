# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    amount_untaxed_unrounded = fields.Float(
        compute="_compute_amount_untaxed_unrounded",
        help="Untaxed amount summed from the unrounded line subtotals, kept at "
        "full precision at the model level. By construction it equals the sum of "
        "the lines' price_subtotal_unrounded, so reports can show a per-line and "
        "a per-document figure that reconcile. Used to disclose the decimals that "
        "the currency-rounded untaxed total hides.",
    )

    @api.depends("invoice_line_ids.price_subtotal_unrounded")
    def _compute_amount_untaxed_unrounded(self):
        for move in self:
            move.amount_untaxed_unrounded = sum(
                move.invoice_line_ids.mapped("price_subtotal_unrounded")
            )
