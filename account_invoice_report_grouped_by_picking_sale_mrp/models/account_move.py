# Copyright 2020 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AccountInvoice(models.Model):
    _inherit = "account.move"

    def _get_signed_quantity_done(self, invoice_line, move, sign):
        res = super()._get_signed_quantity_done(invoice_line, move, sign)
        bom = self.env["mrp.bom"]._bom_find(
            product=invoice_line.product_id, company_id=self.company_id.id
        )
        if bom and bom.type == "phantom":
            bom_line_data = bom.explode(invoice_line.product_id, 1)[1]
            res /= sum(map(lambda r: r[1]["qty"], bom_line_data))
        return res
