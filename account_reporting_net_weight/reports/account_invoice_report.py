# Copyright 2022 Trey, Kilobytes de Soluciones - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models
import odoo.addons.decimal_precision as dp


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    net_weight = fields.Float(
        digits=dp.get_precision("Stock Weight"),
    )

    def _select(self):
        select_str = super()._select()
        select_str += """
            , sub.net_weight as net_weight
            """
        return select_str

    def _sub_select(self):
        select_str = super()._sub_select()
        select_str += """
            , SUM (
                (invoice_type.sign_qty * ail.quantity * pr.net_weight) /
                COALESCE(u.factor,1) * COALESCE(u2.factor,1)) AS net_weight
            """
        return select_str
