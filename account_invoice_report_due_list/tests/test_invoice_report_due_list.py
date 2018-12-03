# -*- coding: utf-8 -*-
# Copyright 2018 Tecnativa - Vicent Cubells <vicent.cubells@tecnativa.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from datetime import timedelta

from odoo.tests import common
from odoo import fields, report


class TestInvoiceReportDueList(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestInvoiceReportDueList, cls).setUpClass()

        cls.payment_term_normal = cls.env['account.payment.term'].create({
            'name': 'One Time Payment Term',
            'line_ids': [(0, 0, {
                'value': 'balance',
                'days': 30,
            })]
        })
        cls.payment_term_multi = cls.env['account.payment.term'].create({
            'name': 'Twice Payment Term',
            'line_ids': [
                (0, 0, {
                    'value': 'percent',
                    'value_amount': 25.0,
                    'days': 30,
                    'sequence': 10,
                }),
                (0, 0, {
                    'value': 'balance',
                    'days': 60,
                    'sequence': 20,
                }),
            ]
        })
        cls.partner = cls.env['res.partner'].create({
            'name': 'Partner test',
        })
        cls.product_id = cls.env['product.product'].create({
            'name': 'Product Test',
        })
        cls.account = cls.env['account.account'].create({
            'name': 'Test Account',
            'code': 'TEST',
            'user_type_id':
                cls.env.ref('account.data_account_type_receivable').id,
            'reconcile': True,

        })
        cls.other_account = cls.env['account.account'].create({
            'name': 'Test Account',
            'code': 'ACC',
            'user_type_id':
                cls.env.ref('account.data_account_type_other_income').id,
            'reconcile': True,

        })

    def test_due_list(self):
        invoice = self.env['account.invoice'].create({
            'partner_id': self.partner.id,
            'payment_term_id': self.payment_term_normal.id,
            'type': 'out_invoice',
            'account_id': self.account.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product_id.id,
                'price_unit': 100.0,
                'account_id': self.other_account.id,
                'name': self.product_id.name,
            })]
        })
        self.assertFalse(invoice.multi_due)
        invoice.payment_term_id = self.payment_term_multi.id
        invoice._onchange_payment_term_date_invoice()
        invoice.action_invoice_open()
        self.assertTrue(invoice.multi_due)
        self.assertEqual(len(invoice.multi_date_due.split()), 2)
        due_date = fields.Date.to_string(
            fields.date.today() + timedelta(days=60))
        (res, _) = report.render_report(
            self.env.cr, self.env.uid,
            [invoice.id], 'account.report_invoice', {})
        self.assertRegexpMatches(res, due_date)
        self.assertRegexpMatches(res, '75.0')
