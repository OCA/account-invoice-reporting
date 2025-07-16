# Copyright 2025 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import fields, models

REPORT_STICKER_POSITIONS = [
    ("top_right", "Top (right)"),
    ("bottom_left", "Bottom (left)"),
]


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    show_product_stickers = fields.Selection(
        string="Product Stickers",
        selection=REPORT_STICKER_POSITIONS,
        help="Display Product Stickers on chosen position inside the report.",
        config_parameter="account_invoice_report_product_sticker.show_product_stickers",
    )
