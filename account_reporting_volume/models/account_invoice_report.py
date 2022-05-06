# Copyright 2022 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    volume = fields.Float(digits="Volume")

    def _select(self):
        select_str = super()._select()
        select_str += """
            , SUM(product.volume * (
                CASE
                WHEN move.type IN ('in_invoice','out_refund','in_receipt') THEN -1
                ELSE 1 END
            ) * line.quantity
            / uom_line.factor * uom_template.factor)
            as volume
            """
        return select_str
