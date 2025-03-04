# Copyright 2025 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import api, fields, models

from .res_config_settings import REPORT_STICKER_POSITIONS


class AccountMove(models.Model):
    _inherit = "account.move"

    show_product_stickers = fields.Selection(
        selection=REPORT_STICKER_POSITIONS,
        compute="_compute_show_product_stickers",
        store=True,
        readonly=False,
        help="Display Product Stickers on chosen position inside the report.",
    )
    sticker_ids = fields.Many2many(
        comodel_name="product.sticker",
        string="Stickers",
        compute="_compute_sticker_ids",
        compute_sudo=True,
        store=False,
    )

    @api.depends("move_type")
    def _compute_show_product_stickers(self):
        self.show_product_stickers = False
        default_sticker_position = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param(
                "account_invoice_report_product_sticker.show_product_stickers", False
            )
        )
        for move in self:
            if not move.is_sale_document(include_receipts=False):
                continue
            move.show_product_stickers = default_sticker_position

    @api.depends("show_product_stickers", "line_ids.product_id")
    def _compute_sticker_ids(self):
        self.sticker_ids = False
        for move in self:
            if not move.show_product_stickers:
                continue
            move.sticker_ids = move.line_ids.product_id.get_product_stickers(
                extra_domain=[
                    "|",
                    ("available_model_ids.model", "in", [self._name]),
                    ("available_model_ids", "=", False),
                ]
            )
