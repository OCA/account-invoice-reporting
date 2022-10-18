# Copyright 2017 Simone Rubino - Agile Business Group
# Copyright 2018 Tecnativa - Pedro M. Baeza
# Copyright 2021 Tecnativa - Víctor Martínez
# Copyright 2022 Bloopark systems - Achraf Mhadhbi
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestAccountInvoiceReport(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        cls.base_comment_model = cls.env["base.comment.template"]
        cls.move_obj = cls.env.ref("account.model_account_move")
        cls.before_comment = cls._create_comment(cls, position="before_lines")
        cls.after_comment = cls._create_comment(cls, position="after_lines")
        cls.partner_a.base_comment_template_ids = [
            (4, cls.before_comment.id),
            (4, cls.after_comment.id),
        ]
        cls.invoice = cls.init_invoice(
            "out_invoice", products=cls.product_a + cls.product_b
        )

    def _create_comment(self, position):
        return self.base_comment_model.create(
            {
                "name": "Comment " + position,
                "company_id": self.company_data["company"].id,
                "position": position,
                "text": "Text " + position,
                "model_ids": [(6, 0, self.move_obj.ids)],
            }
        )

    def test_comments_in_invoice_report(self):
        res = self.env["ir.actions.report"]._render_qweb_html(
            "account.report_invoice", self.invoice.ids
        )
        self.assertRegex(str(res[0]), self.before_comment.text)
        self.assertRegex(str(res[0]), self.after_comment.text)

    def test_comments_in_invoice(self):
        new_invoice = self.init_invoice(
            "out_invoice", products=self.product_a + self.product_b
        )
        new_invoice._compute_comment_template_ids()
        self.assertTrue(self.after_comment in new_invoice.comment_template_ids)
        self.assertTrue(self.before_comment in new_invoice.comment_template_ids)
