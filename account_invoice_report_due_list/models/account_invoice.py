# -*- coding: utf-8 -*-
# Copyright 2018 Carlos Dauden - Tecnativa <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    multi_due = fields.Boolean(
        string='Multiple date due',
        compute='_compute_multi_due'
    )
    multi_date_due = fields.Char(
        string='Due Dates',
        compute='_compute_multi_date_due'
    )

    @api.depends('payment_term_id')
    def _compute_multi_due(self):
        for invoice in self:
            invoice.multi_due = len(invoice.payment_term_id.line_ids) > 1

    @api.depends('move_id', 'payment_term_id', 'date_invoice')
    def _compute_multi_date_due(self):
        lang = self.env.context.get('lang') or 'en_US'
        date_format = self.env['res.lang']._lang_get(lang).date_format
        for invoice in self:
            invoice.multi_date_due = ' '.join(
                fields.Date.from_string(due[0]).strftime(date_format)
                for due in invoice.get_multi_due_list())

    def get_multi_due_list(self):
        self.ensure_one()
        due_list = []
        if self.move_id:
            if self.type in ['in_invoice', 'out_refund']:
                due_move_line_ids = self.move_id.line_ids.filtered(
                    lambda ml: ml.account_id.internal_type == 'payable'
                )
            else:
                due_move_line_ids = self.move_id.line_ids.filtered(
                    lambda ml: ml.account_id.internal_type == 'receivable'
                )
            if self.currency_id != self.company_id.currency_id:
                due_list = [
                    (ml.date_maturity, ml.amount_currency)
                    for ml in due_move_line_ids]
            else:
                due_list = [
                    (ml.date_maturity, ml.balance)
                    for ml in due_move_line_ids]
        elif self.payment_term_id:
            date_invoice = (
                self.date_invoice or fields.Date.context_today(self))
            due_list = self.payment_term_id.with_context(
                currency_id=self.company_id.currency_id.id).compute(
                value=self.amount_total, date_ref=date_invoice)[0]
        due_list.sort()
        return due_list
