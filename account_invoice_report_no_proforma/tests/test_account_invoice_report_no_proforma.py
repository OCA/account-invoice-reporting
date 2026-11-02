# Copyright 2026 Tecnativa - Carlos Lopez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestAccountInvoiceReportNoProforma(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.invoice = cls.init_invoice("out_invoice", amounts=[100], post=True)

    def test_download_pdf_without_proforma(self):
        doc = self.invoice._get_invoice_legal_documents("pdf", allow_fallback=True)
        self.assertEqual(doc["filename"], self.invoice._get_invoice_report_filename())
        self.assertNotIn(b"PROFORMA", doc["content"])
        self.assertFalse(self.invoice.invoice_pdf_report_id)

    def test_portal_without_proforma(self):
        html = (
            self.env["ir.actions.report"]
            .with_context(proforma_invoice=True)
            ._render_qweb_html("account.account_invoices", self.invoice.ids)[0]
        )
        self.assertNotIn(b"PROFORMA", html)

    def test_send_wizard_fallback_keeps_proforma(self):
        invoice_data = {"pdf_report": self.env.ref("account.account_invoices")}
        self.env["account.move.send"]._prepare_invoice_proforma_pdf_report(
            self.invoice, invoice_data
        )
        values = invoice_data["proforma_pdf_attachment_values"]
        self.assertEqual(
            values["name"], self.invoice._get_invoice_proforma_pdf_report_filename()
        )
        self.assertIn(b"PROFORMA", values["raw"])
