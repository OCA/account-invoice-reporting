# Copyright 2026 Quartile (https://www.quartile.co)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo import api, fields, models
from odoo.tools import float_compare


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    price_subtotal_unrounded = fields.Float(
        compute="_compute_price_subtotal_unrounded",
        digits="Product Price",
        help="Line subtotal computed without currency rounding. Used in reports "
        "to disclose the decimals that the currency-rounded subtotal hides "
        '(e.g. under "Round Globally" with a zero-decimal currency).',
    )
    is_price_subtotal_rounded = fields.Boolean(
        compute="_compute_price_subtotal_unrounded",
        help="True when the currency-rounded subtotal differs from the "
        "unrounded one, i.e. rounding hides decimals.",
    )

    @api.depends("price_unit", "quantity", "discount", "price_subtotal")
    def _compute_price_subtotal_unrounded(self):
        precision = self.env["decimal.precision"].precision_get("Product Price")
        for line in self:
            unrounded = line.price_unit * line.quantity * (1 - line.discount / 100.0)
            line.price_subtotal_unrounded = unrounded
            line.is_price_subtotal_rounded = bool(
                float_compare(
                    unrounded, line.price_subtotal, precision_digits=precision
                )
            )
