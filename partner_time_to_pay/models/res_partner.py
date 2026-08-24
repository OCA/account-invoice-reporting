# Copyright (C) 2019 Open Source Integrators
# Copyright 2022 - Moduon
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    # Suppliers
    d2p_life = fields.Float(
        compute="_compute_d2x",
        string="AVG Days to Payable (lifetime)",
        store=True,
        help="Average days of payment for incoming invoices.",
    )
    d2p_ytd = fields.Float(
        compute="_compute_d2x",
        string="AVG Days to Payable (YTD)",
        store=True,
        help="Average days of payment for incoming invoices this year.",
    )
    d2p_ly = fields.Float(
        compute="_compute_d2x",
        string="AVG Days to Payable (LY)",
        store=True,
        help="Average days of payment for incoming invoices last year.",
    )
    # Customers
    d2r_life = fields.Float(
        compute="_compute_d2x",
        string="AVG Days to Receivable (lifetime)",
        store=True,
        help="Average days of payment for outgoing invoices.",
    )
    d2r_ytd = fields.Float(
        compute="_compute_d2x",
        string="AVG Days to Receivable (YTD)",
        store=True,
        help="Average days of payment for outgoing invoices this year.",
    )
    d2r_ly = fields.Float(
        compute="_compute_d2x",
        string="AVG Days to Receivable (LY)",
        store=True,
        help="Average days of payment for outgoing invoices last year.",
    )

    @api.depends("invoice_ids.full_reconcile_payment_date")
    def _compute_d2x(self):
        for partner in self:
            (
                partner.d2r_ly,
                partner.d2r_ytd,
                partner.d2r_life,
            ) = partner._compute_d2x_per_invoice_type(
                (partner + partner.child_ids).invoice_ids, {"out_invoice"}
            )
            (
                partner.d2p_ly,
                partner.d2p_ytd,
                partner.d2p_life,
            ) = partner._compute_d2x_per_invoice_type(
                (partner + partner.child_ids).invoice_ids, {"in_invoice"}
            )

    def _compute_d2x_per_invoice_type(self, invoices, invoice_types):
        self.ensure_one()
        this_year = fields.Date.today().year
        last_year = this_year - 1

        total_number_of_invoices_life, total_days_to_pay_life = 0, 0
        total_number_of_invoices_ytd, total_days_to_pay_ytd = 0, 0
        total_number_of_invoices_ly, total_days_to_pay_ly = 0, 0
        d2x_ly, d2x_ytd, d2x_life = 0, 0, 0

        selected_invoices = invoices.filtered(
            lambda inv: inv.move_type in invoice_types
            and inv.full_reconcile_payment_date
            and inv.state == "posted"
        )
        for invoice in selected_invoices:
            days_until_invoice_is_paid = (
                invoice.full_reconcile_payment_date - invoice.invoice_date
            ).days

            total_number_of_invoices_life += 1
            total_days_to_pay_life += days_until_invoice_is_paid

            if invoice.invoice_date.year == last_year:
                total_number_of_invoices_ly += 1
                total_days_to_pay_ly += days_until_invoice_is_paid

            if invoice.invoice_date.year == this_year:
                total_number_of_invoices_ytd += 1
                total_days_to_pay_ytd += days_until_invoice_is_paid

        if total_number_of_invoices_ly:
            d2x_ly = total_days_to_pay_ly / total_number_of_invoices_ly

        if total_number_of_invoices_ytd:
            d2x_ytd = total_days_to_pay_ytd / total_number_of_invoices_ytd

        if total_number_of_invoices_life:
            d2x_life = total_days_to_pay_life / total_number_of_invoices_life

        return d2x_ly, d2x_ytd, d2x_life
