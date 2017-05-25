# -*- coding: utf-8 -*-
# Copyright 2017 Ursa Information Systems <http://www.ursainfosystems.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    d2p_life = fields.Float(compute='_compute_dtp_life',
                            string='AVG Days to Pay (lifetime)')
    d2p_ytd = fields.Float(compute='_compute_dtp_ytd',
                           string='AVG Days to Pay (YTD)')
    d2r_life = fields.Float(compute='_compute_dtr_life',
                            string='AVG Days to Pay (lifetime)')
    d2r_ytd = fields.Float(compute='_compute_dtr_ytd',
                           string='AVG Days to Pay (YTD)')

    @api.multi
    def _get_invoice_ids(self, partner_id, type):
        return self.env['account.invoice'].search([
            ('partner_id', '=', partner_id),
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

    @api.multi
    def _get_avg_pay_days(self, invoice_ids, life=False):
        average_days_to_pay = 0
        total_days_to_pay = 0
        total_number_of_invoices = 0
        for invoice in invoice_ids:
            total_number_of_invoices += 1
            date_due = fields.Date.from_string(invoice.date_invoice)
            days_to_pay_invoice = 0
            if life:
                days_to_pay_invoice = self._get_invoice_payment(invoice.payment_ids, date_due)
            else:
                if fields.Date.from_string(invoice.date_invoice).year ==\
                        datetime.now().year:
                    days_to_pay_invoice = self._get_invoice_payment(invoice.payment_ids, date_due)
            total_days_to_pay = total_days_to_pay + days_to_pay_invoice
            average_days_to_pay = total_days_to_pay / \
                total_number_of_invoices
        return average_days_to_pay

    @api.multi
    def _compute_dtp_life(self):

        for partner in self:
            invoice_ids = self._get_invoice_ids(partner.id, 'out_invoice')
            partner.d2p_life = self._get_avg_pay_days(invoice_ids, True)

    @api.multi
    def _compute_dtp_ytd(self):

        for partner in self:
            invoice_ids = self._get_invoice_ids(partner.id, 'out_invoice')
            partner.d2p_ytd = self._get_avg_pay_days(invoice_ids)

    @api.multi
    def _compute_dtr_life(self):

        for partner in self:
            invoice_ids = self._get_invoice_ids(partner.id, 'in_invoice')
            partner.d2r_life = self._get_avg_pay_days(invoice_ids, True)

    @api.multi
    def _compute_dtr_ytd(self):

        for partner in self:
            invoice_ids = self._get_invoice_ids(partner.id, 'in_invoice')
            partner.d2r_ytd = self._get_avg_pay_days(invoice_ids)
