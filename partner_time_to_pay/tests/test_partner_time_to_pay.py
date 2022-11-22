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
            }
        )
        self.time_to_pay_days = 10
        product = self.env.ref("product.product_product_4")
        # Create invoice
        move_form = Form(am_model.with_context(default_move_type="out_invoice"))
        move_form.partner_id = self.partner
        move_form.invoice_date = today
        with move_form.invoice_line_ids.new() as line_form:
            line_form.product_id = product
            line_form.price_unit = 100.0
            line_form.quantity = 10.0
        invoice = move_form.save()
        invoice.action_post()
        # Create payment
        apr_model.with_context(
            active_model="account.move", active_ids=invoice.ids
        ).create(
            {
                "payment_date": invoice.date + timedelta(days=self.time_to_pay_days),
            }
        ).with_context(
            dont_redirect_to_payments=True,
        ).action_create_payments()

    def test_partner_compute_d2x(self):
        self.assertEqual(self.partner.d2r_ytd, self.time_to_pay_days)
        self.assertEqual(self.partner.d2r_life, self.time_to_pay_days)
