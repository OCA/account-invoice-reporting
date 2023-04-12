# Copyright (C) 2019 Serpent Consulting Services Pvt. Ltd.
#   (<http://www.serpentcs.com>)
# Copyright 2022 - Moduon
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import fields
from odoo.tests import Form, TransactionCase


class TestPartnerTimeToPay(TransactionCase):
    def setUp(self):
        super(TestPartnerTimeToPay, self).setUp()
        apr_model = self.env["account.payment.register"]
        am_model = self.env["account.move"]
        rp_model = self.env["res.partner"]
        today = fields.Date.today()
        self.partner = rp_model.create(
            {
                "name": "Test Time to Pay Partner",
                "is_company": True,
                "child_ids": [(0, 0, {"name": "TTPP Contact", "type": "invoice"})],
            }
        )
        self.time_to_pay_days = 10
        product = self.env.ref("product.product_product_4")
        # Create invoice for last year
        move_form_ly = Form(am_model.with_context(default_move_type="out_invoice"))
        move_form_ly.partner_id = self.partner.child_ids[0]
        move_form_ly.invoice_date = today - timedelta(days=365)
        with move_form_ly.invoice_line_ids.new() as line_form_ly:
            line_form_ly.product_id = product
            line_form_ly.price_unit = 100.0
            line_form_ly.quantity = 10.0
        invoice_ly = move_form_ly.save()
        invoice_ly.action_post()
        # Create payment for last year
        apr_model.with_context(
            active_model="account.move", active_ids=invoice_ly.ids
        ).create(
            {
                "payment_date": invoice_ly.date + timedelta(days=self.time_to_pay_days),
            }
        ).with_context(
            dont_redirect_to_payments=True,
        ).action_create_payments()
        # Create invoice for this year
        move_form_ty = Form(am_model.with_context(default_move_type="out_invoice"))
        move_form_ty.partner_id = self.partner.child_ids[0]
        move_form_ty.invoice_date = today
        with move_form_ty.invoice_line_ids.new() as line_form_ty:
            line_form_ty.product_id = product
            line_form_ty.price_unit = 100.0
            line_form_ty.quantity = 10.0
        invoice_ty = move_form_ty.save()
        invoice_ty.action_post()
        # Create payment for this year
        apr_model.with_context(
            active_model="account.move", active_ids=invoice_ty.ids
        ).create(
            {
                "payment_date": invoice_ty.date + timedelta(days=self.time_to_pay_days),
            }
        ).with_context(
            dont_redirect_to_payments=True,
        ).action_create_payments()

    def test_partner_compute_d2x(self):
        self.assertEqual(self.partner.child_ids[0].d2r_ly, self.time_to_pay_days)
        self.assertEqual(self.partner.child_ids[0].d2r_ytd, self.time_to_pay_days)
        self.assertEqual(self.partner.child_ids[0].d2r_life, self.time_to_pay_days)
        self.assertEqual(self.partner.d2r_ly, self.time_to_pay_days)
        self.assertEqual(self.partner.d2r_ytd, self.time_to_pay_days)
        self.assertEqual(self.partner.d2r_life, self.time_to_pay_days)
