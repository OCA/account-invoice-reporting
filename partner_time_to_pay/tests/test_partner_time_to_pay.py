# Copyright (C) 2019 Serpent Consulting Services Pvt. Ltd.
#   (<http://www.serpentcs.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo.fields import Date
from odoo.tests.common import TransactionCase


class TestPartnerTimeToPay(TransactionCase):
    def setUp(self):
        super(TestPartnerTimeToPay, self).setUp()
        self.payment_model = self.env["account.payment"]
        self.register_payments_model = self.env["account.payment.register"]
        self.partner_id = self.env.ref("base.res_partner_1")
        self.product_id = self.env.ref("product.product_product_4")
        self.account_model = self.env["account.account"]
        self.account_move_model = self.env["account.move"]
        self.account_journal = self.env["account.journal"]
        self.payment_method_manual_in = self.env.ref(
            "account.account_payment_method_manual_in"
        )
        self.account_receivable_id = self.env.ref(
            "account.data_account_type_receivable"
        )
        self.account_revenue_id = self.env.ref("account.data_account_type_revenue")
        self.account_revenue = self.account_model.search(
            [("user_type_id", "=", self.account_revenue_id.id)], limit=1
        )
        self.today = Date.from_string(Date.context_today(self.env.user))

        self.invoice_id = self.account_move_model.create(
            {
                "partner_id": self.partner_id.id,
                "type": "out_invoice",
                "invoice_date": self.today,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product_id.id,
                            "name": self.product_id.name,
                            "price_unit": 100,
                            "quantity": 10,
                            "account_id": self.account_revenue.id,
                        },
                    )
                ],
            }
        )

        self.invoice_id._onchange_invoice_line_ids()
        self.invoice_id._onchange_recompute_dynamic_lines()
        self.invoice_id.action_post()
        self.bank_journal_euro = self.account_journal.create(
            {"name": "Bank", "type": "bank", "code": "BNK67"}
        )

        ctx = {"active_model": "account.invoice", "active_ids": [self.invoice_id.id]}
        self.register_payments = self.register_payments_model.with_context(ctx).create(
            {
                "payment_date": self.today + relativedelta(days=10),
                "journal_id": self.bank_journal_euro.id,
                "payment_method_id": self.payment_method_manual_in.id,
            }
        )
        self.register_payments.create_payments()
        self.payment = self.payment_model.search([], order="id desc", limit=1)

    def test_partner_compute_d2x(self):
        check_d2p_ytd = self.partner_id.d2p_ytd
        check_d2p_life = self.partner_id.d2p_life
        self.partner_id._compute_d2x()
        self.assertEqual(check_d2p_ytd, self.partner_id.d2p_ytd)
        self.assertEqual(check_d2p_life, self.partner_id.d2p_ytd)
        self.assertNotEqual(check_d2p_ytd, self.partner_id.d2r_ytd)
        self.assertNotEqual(check_d2p_life, self.partner_id.d2r_life)
