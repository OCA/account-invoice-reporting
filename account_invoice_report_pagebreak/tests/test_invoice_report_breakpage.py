from lxml import html

from odoo.tests import tagged
from odoo.tools.image import image_data_uri

from odoo.addons.account.tests.common import TestAccountReconciliationCommon


@tagged("post_install", "-at_install")
class TestInvoiceReportAvoidPageBreakInSection(TestAccountReconciliationCommon):
    def setUp(self):
        super().setUp()
        self.invoice = self.create_invoice_partner()
        self.invoice.line_ids.create(
            [
                {
                    "move_id": self.invoice.id,
                    "name": "Note 1",
                    "display_type": "line_note",
                    "sequence": 20,
                },
                {
                    "move_id": self.invoice.id,
                    "name": "Note 2",
                    "display_type": "line_note",
                    "sequence": 40,
                },
            ]
        )

    def test_sale_report_with_section(self):
        self.invoice.line_ids.create(
            [
                {
                    "move_id": self.invoice.id,
                    "name": "Section",
                    "display_type": "line_section",
                    "sequence": 30,
                },
            ]
        )
        doc = html.document_fromstring(
            self.env["ir.qweb"]
            ._render(
                "account.report_invoice_document",
                values={
                    "o": self.invoice,
                    "env": self.env,
                    "company": self.env.company,
                    "image_data_uri": image_data_uri,
                },
            )
            .decode("utf-8")
        )
        self.assertEqual(
            len(doc.find('.//table[@style="page-break-inside: avoid"]')), 2
        )

    def test_sale_report_without_section(self):
        doc = html.document_fromstring(
            self.env["ir.qweb"]
            ._render(
                "account.report_invoice_document",
                values={
                    "o": self.invoice,
                    "env": self.env,
                    "company": self.env.company,
                    "image_data_uri": image_data_uri,
                },
            )
            .decode("utf-8")
        )
        self.assertFalse(doc.find('.//table[@style="page-break-inside: avoid"]'))
