# Copyright 2017 Tecnativa - Pedro M. Baeza
# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    weight = fields.Float(digits="Stock Weight")

    def _select(self):
        select_str = super()._select()
        select_str += """
            , COALESCE(
                (product.weight * (
                    CASE
                    WHEN move.move_type IN ('in_invoice','out_refund','in_receipt') THEN -1
                    ELSE 1 END
                ) * line.quantity
                / uom_line.factor * uom_template.factor
            ), 0.0) as weight
            """
        return select_str
