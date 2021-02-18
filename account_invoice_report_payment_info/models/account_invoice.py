# Copyright 2020 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class AccountInvoice(models.Model):
    _inherit = "account.move"

    def _get_reconciled_info_JSON_values(self):
        res = super()._get_reconciled_info_JSON_values()
        if not res:
            return res
        info_pattern = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("account_invoice_report_payment_info.info_pattern", default="")
        )
        Payment = self.env["account.move.line"]
        for payment_dict in res:
            payment = Payment.browse(payment_dict["payment_id"])
            payment_dict["move_ref"] = payment.move_id.ref
            payment_dict["extra_info"] = info_pattern.format(**payment_dict)
        return res
