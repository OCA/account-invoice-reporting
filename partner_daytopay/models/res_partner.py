# -*- coding: utf-8 -*-
# Copyright 2017 Ursa Information Systems <http://www.ursainfosystems.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    d2p_life = fields.Float(compute='_compute_d2x',
                            string='AVG Days to Pay (lifetime)')
    d2p_ytd = fields.Float(compute='_compute_d2x',
                           string='AVG Days to Pay (YTD)')
    d2r_life = fields.Float(compute='_compute_d2x',
                            string='AVG Days to Pay (lifetime)')
    d2r_ytd = fields.Float(compute='_compute_d2x',
                           string='AVG Days to Pay (YTD)')

    def _compute_d2x(self):
        for partner in self:
            partner.d2p_ytd, partner.d2p_life = \
                self._compute_d2x_per_invoice_type(partner, 'out_invoice')
            partner.d2r_ytd, partner.d2r_life = \
                self._compute_d2x_per_invoice_type(partner, 'in_invoice')

    def _compute_d2x_per_invoice_type(self, partner, invoice_type):

        this_year = datetime.now().year

        total_number_of_invoices_life = 0
        total_number_of_invoices_ytd = 0

        total_days_to_pay_life = 0
        total_days_to_pay_ytd = 0

        d2x_ytd = 0
        d2x_life = 0

        for invoice in self._get_invoice_ids(partner.id, invoice_type):

            invoice_year = fields.Date.from_string(invoice.date_invoice).year

            date_due = fields.Date.from_string(invoice.date_invoice)

            days_to_pay_invoice = self._get_invoice_payment(
                invoice.payment_ids, date_due)

            total_number_of_invoices_life += 1
            total_days_to_pay_life += days_to_pay_invoice

            if invoice_year == this_year:
                total_number_of_invoices_ytd += 1
                total_days_to_pay_ytd += days_to_pay_invoice

        try:
            d2x_ytd = total_days_to_pay_ytd / total_number_of_invoices_ytd
        except ZeroDivisionError:
            d2x_ytd = 0
        try:
            d2x_life = total_days_to_pay_life / total_number_of_invoices_life
        except ZeroDivisionError:
            d2x_life = 0

        return d2x_ytd, d2x_life

    @api.multi
    def _get_invoice_ids(self, partner_id, type):
        return self.env['account.invoice'].search([
            '|'
            ('partner_id', '=', partner_id),
            ('partner_id.parent_id', '=', partner_id),
            ('state', '=', 'paid'),
            ('type', '=', type)
        ])

    @api.multi
    def _get_invoice_payment(self, payment_ids, date_due):
        days_for_latest_payment = 0
        for payment in payment_ids:
            if payment.state == 'posted':
                days_for_this_payment = (
                    fields.Date.from_string(payment.payment_date) -
                    date_due).days
                if days_for_this_payment < 0:
                    days_for_this_payment = 0
                if days_for_this_payment > days_for_latest_payment:
                    days_for_latest_payment = days_for_this_payment
        return days_for_latest_payment
