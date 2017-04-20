# -*- coding: utf-8 -*-
# Copyright 2017 Ursa Information Systems <http://www.ursainfosystems.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from datetime import datetime
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def _compute_dtp_life(self):

        for partner in self:
            average_days_to_pay = 0
            total_days_to_pay = 0
            total_number_of_invoices = 0
            invoice_domain = [('partner_id', '=', partner.id),
                              ('state', '=', 'paid'),
                              ('type', '=', 'out_invoice')]
            invoice_ids = partner.env['account.invoice'].search(invoice_domain)
            for invoice in invoice_ids:
                total_number_of_invoices += 1
                date_due = invoice.date_invoice
                days_for_latest_payment = 0

                for payment in invoice.payment_ids:
                    if payment.state == 'posted':
                        days_for_this_payment = \
                            (datetime.strptime(payment.payment_date,
                                               '%Y-%m-%d') -
                             datetime.strptime(date_due, '%Y-%m-%d')).days
                        if days_for_this_payment < 0:
                            days_for_this_payment = 0
                        if days_for_this_payment > days_for_latest_payment:
                            days_for_latest_payment = days_for_this_payment

                days_to_pay_invoice = days_for_latest_payment
                total_days_to_pay = total_days_to_pay + days_to_pay_invoice
                average_days_to_pay = total_days_to_pay / \
                    total_number_of_invoices

            partner.d2p_life = average_days_to_pay

    @api.multi
    def _compute_dtp_ytd(self):

        for partner in self:
            average_days_to_pay = 0
            total_days_to_pay = 0
            total_number_of_invoices = 0
            invoice_domain = [('partner_id', '=', partner.id),
                              ('state', '=', 'paid'),
                              ('type', '=', 'out_invoice')]
            invoice_ids = partner.env['account.invoice'].search(invoice_domain)
            for invoice in invoice_ids:
                if datetime.strptime(invoice.date_invoice, '%Y-%m-%d').year ==\
                        datetime.now().year:
                    total_number_of_invoices += 1
                    date_due = invoice.date_invoice
                    days_for_latest_payment = 0

                    for payment in invoice.payment_ids:
                        if payment.state == 'posted':
                            days_for_this_payment = (
                                datetime.strptime(payment.payment_date,
                                                  '%Y-%m-%d') -
                                datetime.strptime(date_due, '%Y-%m-%d')).days
                            if days_for_this_payment < 0:
                                days_for_this_payment = 0
                            if days_for_this_payment > days_for_latest_payment:
                                days_for_latest_payment = days_for_this_payment
                    days_to_pay_invoice = days_for_latest_payment
                    total_days_to_pay = total_days_to_pay + days_to_pay_invoice
                    average_days_to_pay = total_days_to_pay / \
                        total_number_of_invoices

            partner.d2p_ytd = average_days_to_pay

    @api.multi
    def _compute_dtr_life(self):

        for partner in self:
            average_days_to_pay = 0
            total_days_to_pay = 0
            total_number_of_invoices = 0
            invoice_domain = [('partner_id', '=', partner.id),
                              ('state', '=', 'paid'),
                              ('type', '=', 'in_invoice')]
            invoice_ids = partner.env['account.invoice'].search(invoice_domain)
            for invoice in invoice_ids:
                total_number_of_invoices += 1
                date_due = invoice.date_invoice
                days_for_latest_payment = 0

                for payment in invoice.payment_ids:
                    if payment.state == 'posted':
                        days_for_this_payment = (
                            datetime.strptime(payment.payment_date,
                                              '%Y-%m-%d') -
                            datetime.strptime(date_due, '%Y-%m-%d')).days
                        if days_for_this_payment < 0:
                            days_for_this_payment = 0
                        if days_for_this_payment > days_for_latest_payment:
                            days_for_latest_payment = days_for_this_payment
                days_to_pay_invoice = days_for_latest_payment
                total_days_to_pay = total_days_to_pay + days_to_pay_invoice
                average_days_to_pay = total_days_to_pay / \
                    total_number_of_invoices

            partner.d2r_life = average_days_to_pay

    @api.multi
    def _compute_dtr_ytd(self):

        for partner in self:
            total_days_to_pay = 0
            average_days_to_pay = 0
            total_number_of_invoices = 0
            invoice_domain = [('partner_id', '=', partner.id),
                              ('state', '=', 'paid'),
                              ('type', '=', 'in_invoice')]
            invoice_ids = partner.env['account.invoice'].search(invoice_domain)
            for invoice in invoice_ids:
                if datetime.strptime(invoice.date_invoice, '%Y-%m-%d').year ==\
                        datetime.now().year:
                    total_number_of_invoices += 1
                    date_due = invoice.date_invoice
                    days_for_latest_payment = 0

                    for payment in invoice.payment_ids:
                        if payment.state == 'posted':
                            days_for_this_payment = (
                                datetime.strptime(payment.payment_date,
                                                  '%Y-%m-%d') -
                                datetime.strptime(date_due, '%Y-%m-%d')).days
                            if days_for_this_payment < 0:
                                days_for_this_payment = 0
                            if days_for_this_payment > days_for_latest_payment:
                                days_for_latest_payment = days_for_this_payment

                    days_to_pay_invoice = days_for_latest_payment
                    total_days_to_pay = total_days_to_pay + days_to_pay_invoice
                    average_days_to_pay = total_days_to_pay / \
                        total_number_of_invoices

            partner.d2r_ytd = average_days_to_pay

    d2p_life = fields.Float(compute=_compute_dtp_life,
                            string='AVG Days to Pay (lifetime)')
    d2p_ytd = fields.Float(compute=_compute_dtp_ytd,
                           string='AVG Days to Pay (YTD)')
    d2r_life = fields.Float(compute=_compute_dtr_life,
                            string='AVG Days to Pay (lifetime)')
    d2r_ytd = fields.Float(compute=_compute_dtr_ytd,
                           string='AVG Days to Pay (YTD)')
