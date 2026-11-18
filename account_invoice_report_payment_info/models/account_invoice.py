# Copyright 2020 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _prepare_payments_widget_reconciled_info(self, partial_info):
        payment_dict = super()._prepare_payments_widget_reconciled_info(partial_info)
        info_pattern = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_str("account_invoice_report_payment_info.info_pattern", default="")
        )
        move = partial_info["aml"].move_id
        payment_dict["move_ref"] = move.ref
        payment_dict["extra_info"] = (
            info_pattern.format(**payment_dict) if info_pattern else ""
        )
        return payment_dict
