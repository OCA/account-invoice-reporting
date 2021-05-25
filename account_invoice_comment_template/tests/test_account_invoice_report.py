# Copyright 2017 Simone Rubino - Agile Business Group
# Copyright 2018 Tecnativa - Pedro M. Baeza
# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import Form, TransactionCase


class TestAccountInvoiceReport(TransactionCase):
    def setUp(self):
        super().setUp()
        self.company = self.env.ref("base.main_company")
        self.base_comment_model = self.env["base.comment.template"]
        self.move_obj = self.env.ref("account.model_account_move")
        self.before_comment = self._create_comment("before_lines")
        self.after_comment = self._create_comment("after_lines")
        self.partner = self.env["res.partner"].create({"name": "Partner Test"})
        self.partner.base_comment_template_ids = [
            (4, self.before_comment.id),
            (4, self.after_comment.id),
        ]
        self.income_account = self.env["account.account"].search(
            [("user_type_id.name", "=", "Income")], limit=1
        )
        self.journal_sale = self.env["account.journal"].create(
            {
                "name": "Test journal sale",
                "code": "TST-JRNL-S",
                "type": "sale",
                "company_id": self.company.id,
            }
        )
        move_form = self._create_invoice()
        self.invoice = move_form.save()

    def _create_invoice(self):
        move_form = Form(
            self.env["account.move"].with_context(default_type="out_invoice")
        )
        move_form.partner_id = self.partner
        move_form.journal_id = self.journal_sale
        with move_form.invoice_line_ids.new() as line_form:
            line_form.name = "test"
            line_form.quantity = 1.0
            line_form.price_unit = 100
            line_form.account_id = self.income_account
        return move_form

    def _create_comment(self, position):
        return self.base_comment_model.create(
            {
                "name": "Comment " + position,
                "company_id": self.company.id,
                "position": position,
                "text": "Text " + position,
                "model_ids": [(6, 0, self.move_obj.ids)],
            }
        )

    def test_comments_in_invoice_report(self):
        res = (
            self.env["ir.actions.report"]
            ._get_report_from_name("account.report_invoice")
            .render_qweb_html(self.invoice.ids)
        )
        self.assertRegexpMatches(str(res[0]), self.before_comment.text)
        self.assertRegexpMatches(str(res[0]), self.after_comment.text)

    def test_comments_in_invoice(self):
        move_form = self._create_invoice()
        new_invoice = move_form.save()
        new_invoice._compute_comment_template_ids()
        self.assertTrue(self.after_comment in new_invoice.comment_template_ids)
        self.assertTrue(self.before_comment in new_invoice.comment_template_ids)
