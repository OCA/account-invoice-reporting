# Copyright 2026 Heliconia Solutions - Bhavesh
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestAccountInvoiceReportPaymentInfo(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.invoice = cls.init_invoice(
            "out_invoice",
            partner=cls.partner_a,
            products=cls.product_a,
        )
        cls.invoice.action_post()

    def test_payment_info_in_widget_and_report(self):
        payment = (
            self.env["account.payment.register"]
            .with_context(active_model="account.move", active_ids=self.invoice.ids)
            .create({"payment_date": "2024-01-01"})
            ._create_payments()
        )
        payment.move_id.ref = "PAY-REF-001"
        self.invoice.invalidate_recordset()
        widget = self.invoice.invoice_payments_widget
        self.assertTrue(widget)
        self.assertEqual(len(widget["content"]), 1)
        self.assertEqual(widget["content"][0]["move_ref"], "PAY-REF-001")
        self.assertEqual(widget["content"][0]["extra_info"], "(PAY-REF-001)")

        html_report = self.env["ir.actions.report"]._render_qweb_html(
            "account.report_invoice_with_payments", self.invoice.ids
        )[0]
        self.assertIn("(PAY-REF-001)", html_report.decode())

        self.env["ir.config_parameter"].sudo().set_param(
            "account_invoice_report_payment_info.info_pattern", "Ref: {move_ref}"
        )
        self.invoice.invalidate_recordset()
        self.assertEqual(
            self.invoice.invoice_payments_widget["content"][0]["extra_info"],
            "Ref: PAY-REF-001",
        )
