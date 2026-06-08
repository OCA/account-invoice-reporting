# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    price_subtotal_unrounded = fields.Float(
        compute="_compute_price_subtotal_unrounded",
        help="Line subtotal computed without currency rounding. Kept at full "
        "precision at the model level; reports round it for display using the "
        "company's untaxed-unrounded digits. Used to disclose the decimals that "
        'the currency-rounded subtotal hides (e.g. under "Round Globally" with a '
        "zero-decimal currency).",
    )

    @api.depends("price_unit", "quantity", "discount", "tax_ids", "currency_id")
    def _compute_price_subtotal_unrounded(self):
        # Mirror core's _compute_totals (account.move.line) but keep the value at
        # full precision: read the tax engine's raw_total_excluded_currency, which
        # is the tax-excluded base *before* currency rounding. This strips embedded
        # price-included taxes (e.g. JP consumption tax) just like price_subtotal,
        # so amount_untaxed_unrounded reconciles with amount_untaxed.
        AccountTax = self.env["account.tax"]
        for line in self:
            if line.display_type not in ("product", "cogs"):
                line.price_subtotal_unrounded = 0.0
                continue
            base_line = line.move_id._prepare_product_base_line_for_taxes_computation(
                line
            )
            AccountTax._add_tax_details_in_base_line(base_line, line.company_id)
            line.price_subtotal_unrounded = base_line["tax_details"][
                "raw_total_excluded_currency"
            ]
