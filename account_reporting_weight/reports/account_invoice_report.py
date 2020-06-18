# Copyright 2017 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    weight = fields.Float(digits="Stock Weight")

    def _select(self):
        select_str = super()._select()
        select_str += """
            , SUM(product.weight * line.quantity
            / uom_line.factor * uom_template.factor)
            as weight
            """
        return select_str
