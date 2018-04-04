# -*- coding: utf-8 -*-
# Copyright 2017 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase
from odoo import report


class TestAccountInvoiceReport(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestAccountInvoiceReport, self).setUp()
        self.base_comment_model = self.env['base.comment.template']
        self.before_comment = self._create_comment('before_lines')
        self.after_comment = self._create_comment('after_lines')
        self.partner_id = self.env['res.partner'].create({
            'name': 'Partner Test'
        })
        self.invoice_model = self.env['account.invoice']
        self.invoice = self.invoice_model.create({
            'partner_id': self.env.ref('base.res_partner_1').id,
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
        (res, _) = report. \
            render_report(self.env.cr, self.env.uid,
                          [self.invoice.id], 'account.report_invoice', {})
        self.assertRegexpMatches(res, self.before_comment.text)
        self.assertRegexpMatches(res, self.after_comment.text)

    def test_onchange_partner_id(self):
        self.partner_id.comment_template_id = self.after_comment.id
        vals = {
            'partner_id': self.partner_id.id,
        }
        new_invoice = self.env['account.invoice'].new(vals)
        new_invoice._onchange_partner_id()
        invoice_dict = new_invoice._convert_to_write(new_invoice._cache)
        new_invoice = self.env['account.invoice'].create(invoice_dict)
        self.assertEqual(new_invoice.comment_template2_id, self.after_comment)
        self.partner_id.comment_template_id = self.before_comment.id
        new_invoice = self.env['account.invoice'].new(vals)
        new_invoice._onchange_partner_id()
        invoice_dict = new_invoice._convert_to_write(new_invoice._cache)
        new_invoice = self.env['account.invoice'].create(invoice_dict)
        self.assertEqual(new_invoice.comment_template1_id, self.before_comment)
