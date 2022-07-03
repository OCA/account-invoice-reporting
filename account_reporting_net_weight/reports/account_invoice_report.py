# Copyright 2023 Trey, Kilobytes de Soluciones - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    net_weight = fields.Float(digits="Stock Weight")

    def _select(self):
        select_str = super()._select()
        select_str += """
            , sum(product.net_weight) / NULLIF(COALESCE(uom_line.factor, 1) /
                  COALESCE(uom_template.factor, 1), 0.0) * (
                      CASE WHEN move.type IN (
                          'in_invoice','out_refund','in_receipt')
                      THEN -1 ELSE 1 END)
               AS net_weight
            """
        return select_str
