# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    untaxed_unrounded_digits = fields.Integer(
        default=2,
        help="Number of decimal places used to display the unrounded line "
        "subtotals and untaxed amounts on reports. Set it finer than the company "
        "currency so the decimals that currency rounding hides become visible; "
        "do not set it to the currency's own precision or the original mismatch "
        "reappears.",
    )
