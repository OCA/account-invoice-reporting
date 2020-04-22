# -*- coding: utf-8 -*-
# Copyright 2019 PlanetaTIC - Marc Poch <mpoch@planetatic.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    price_total_with_taxes = fields.Float(string='Total With Taxes',
                                          readonly=True)

    def _select(self):
        select_str = super(AccountInvoiceReport, self)._select()
        select_str += """
            , sub.price_total_with_taxes as price_total_with_taxes
            """
        return select_str

    def _sub_select(self):
        select_str = super(AccountInvoiceReport, self)._sub_select()
        select_str += """
            , SUM(ail.price_unit * invoice_type.sign * (
(invoice_type.sign_qty * ail.quantity) / u.factor * u2.factor) * (
100 - ail.discount) / 100) AS price_total_with_taxes
            """
        return select_str
