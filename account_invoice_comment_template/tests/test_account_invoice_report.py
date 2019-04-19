# Copyright 2017 Simone Rubino - Agile Business Group
# Copyright 2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestAccountInvoiceReport(TransactionCase):
    at_install = False
    post_install = True

    def setUp(self):
        super(TestAccountInvoiceReport, self).setUp()
        self.base_comment_model = self.env['base.comment.template']
        self.before_comment = self._create_comment('before_lines')
        self.after_comment = self._create_comment('after_lines')
        self.partner = self.env['res.partner'].create({
            'name': 'Partner Test'
        })
        self.invoice_model = self.env['account.invoice']
        self.invoice = self.invoice_model.create({
            'partner_id': self.partner.id,
            'comment_template1_id': self.before_comment.id,
            'comment_template2_id': self.after_comment.id
        })

        self.invoice._set_note1()
        self.invoice._set_note2()

    def _create_comment(self, position):
        return self.base_comment_model.create({
            'name': 'Comment ' + position,
            'position': position,
            'text': 'Text ' + position
        })

    def test_comments_in_invoice(self):
        res = self.env['ir.actions.report']._get_report_from_name(
            'account.report_invoice'
        ).render_qweb_html(self.invoice.ids)
        self.assertRegexpMatches(str(res[0]), self.before_comment.text)
        self.assertRegexpMatches(str(res[0]), self.after_comment.text)

    def test_onchange_partner_id(self):
        self.partner.property_comment_template_id = self.after_comment.id
        new_invoice = self.env['account.invoice'].new({
            'partner_id': self.partner.id,
        })
        new_invoice._onchange_partner_id()
        self.assertEqual(new_invoice.comment_template2_id, self.after_comment)
        self.partner.property_comment_template_id = self.before_comment.id
        new_invoice._onchange_partner_id()
        self.assertEqual(new_invoice.comment_template1_id, self.before_comment)
