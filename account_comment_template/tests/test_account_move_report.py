# Copyright 2017 Simone Rubino - Agile Business Group
# Copyright 2018 Tecnativa - Pedro M. Baeza
# Copyright 2021-2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestAccountInvoiceReport(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        cls.env = cls.env(
            context=dict(
                cls.env.context,
                mail_create_nolog=True,
                mail_create_nosubscribe=True,
                mail_notrack=True,
                no_reset_password=True,
                tracking_disable=True,
            )
        )
        cls.base_comment_model = cls.env["base.comment.template"]
        cls.res_model_id = cls.env.ref("account.model_account_move")
        cls.before_comment = cls._create_comment(cls, "before_lines")
        cls.after_comment = cls._create_comment(cls, "after_lines")
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Partner Test",
                "base_comment_template_ids": [
                    (4, cls.before_comment.id),
                    (4, cls.after_comment.id),
                ],
            }
        )
        cls.invoice = cls.init_invoice(
            "out_invoice", partner=cls.partner, products=cls.product_a + cls.product_b
        )

    def _create_comment(self, position):
        return self.base_comment_model.create(
            {
                "name": "Comment " + position,
                "company_id": self.company_data["company"].id,
                "position": position,
                "text": "Text " + position,
                "models": "account.move",
                "model_ids": [(6, 0, self.res_model_id.ids)],
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
            "out_invoice",
            partner=self.partner,
            products=self.product_a + self.product_b,
        )
        new_invoice._compute_comment_template_ids()
        self.assertTrue(self.after_comment in new_invoice.comment_template_ids)
        self.assertTrue(self.before_comment in new_invoice.comment_template_ids)
