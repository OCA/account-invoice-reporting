# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    untaxed_unrounded_digits = fields.Integer(
        related="company_id.untaxed_unrounded_digits",
        readonly=False,
    )
