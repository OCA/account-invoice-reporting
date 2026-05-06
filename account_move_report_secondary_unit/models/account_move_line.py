# © 2026 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    secondary_uom_id = fields.Many2one(
        comodel_name="product.secondary.unit",
        compute="_compute_secondary_uom_id",
    )

    secondary_uom_qty = fields.Float(
        compute="_compute_secondary_uom_id", digits="Product Unit of Measure"
    )

    @api.depends(
        "product_id.sale_secondary_uom_id",
        "product_id.sale_secondary_uom_id.factor",
        "sale_line_ids.secondary_uom_id",
    )
    def _compute_secondary_uom_id(self):
        for record in self:
            secondary_unit = (
                record.sale_line_ids[:1].secondary_uom_id
                or record.product_id.sale_secondary_uom_id
            )
            record.secondary_uom_id = secondary_unit

            if secondary_unit and secondary_unit.factor:
                record.secondary_uom_qty = record.quantity / secondary_unit.factor
