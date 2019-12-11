# Copyright (C) 2019 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    d2p_life = fields.Float(
        compute="_compute_d2x", string="AVG Days to Payable (lifetime)"
    )
    d2p_ytd = fields.Float(compute="_compute_d2x", string="AVG Days to Payable (YTD)")
    d2r_life = fields.Float(
        compute="_compute_d2x", string="AVG Days to Receivable (lifetime)"
    )
    d2r_ytd = fields.Float(
        compute="_compute_d2x", string="AVG Days to Receivable (YTD)"
    )

    def _compute_d2x(self):
        for partner in self:
            partner.d2p_ytd, partner.d2p_life = self._compute_d2x_per_invoice_type(
                partner, "out_invoice"
            )
            partner.d2r_ytd, partner.d2r_life = self._compute_d2x_per_invoice_type(
                partner, "in_invoice"
            )

    def _compute_d2x_per_invoice_type(self, partner, invoice_type):
        this_year = datetime.now().year

        total_number_of_invoices_life = 0
        total_number_of_invoices_ytd = 0

        total_days_to_pay_life = 0
        total_days_to_pay_ytd = 0

        d2x_ytd = 0
        d2x_life = 0

        for invoice in self._get_invoice_ids(partner.id, invoice_type):
            payment_ids = self.env["account.payment"].search(
                [("invoice_ids", "in", [invoice.id])]
            )
            date_due = fields.Date.from_string(invoice.invoice_date)
            invoice_year = date_due.year

            days_to_pay_invoice = self._get_invoice_payment(payment_ids, date_due)
            total_number_of_invoices_life += 1

            total_days_to_pay_life += days_to_pay_invoice

            if invoice_year == this_year:
                total_number_of_invoices_ytd += 1
                total_days_to_pay_ytd += days_to_pay_invoice

        if total_number_of_invoices_ytd != 0:
            d2x_ytd = total_days_to_pay_ytd / total_number_of_invoices_ytd
        else:
            d2x_ytd = 0

        if total_number_of_invoices_life != 0:
            d2x_life = total_days_to_pay_life / total_number_of_invoices_life
        else:
            d2x_life = 0

        return d2x_ytd, d2x_life

    def _get_invoice_ids(self, partner_id, invoice_type):
        return self.env["account.move"].search(
            [
                ("partner_id", "=", partner_id),
                ("invoice_payment_state", "=", "paid"),
                ("type", "=", invoice_type),
            ]
        )

    def _get_invoice_payment(self, payment_time_ids, date_due):
        days_for_latest_payment = 0
        for payment in payment_time_ids:
            if payment.state == "posted":
                days_for_this_payment = (
                    fields.Date.from_string(payment.payment_date) - date_due
                ).days
                if days_for_this_payment < 0:
                    days_for_this_payment = 0
                if days_for_this_payment > days_for_latest_payment:
                    days_for_latest_payment = days_for_this_payment
        return days_for_latest_payment
