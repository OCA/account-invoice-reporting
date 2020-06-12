# Copyright 2020 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def _get_payments_vals(self):
        res = super()._get_payments_vals()
        if not res:
            return res
        info_pattern = self.env['ir.config_parameter'].sudo().get_param(
            'account_invoice_report_payment_info.info_pattern', default='')
        Payment = self.env['account.move.line']
        for payment_dict in res:
            payment = Payment.browse(
                payment_dict['payment_id'], prefetch=self._prefetch)
            payment_dict['move_ref'] = payment.move_id.ref
            payment_dict['extra_info'] = info_pattern.format(**payment_dict)
        return res
