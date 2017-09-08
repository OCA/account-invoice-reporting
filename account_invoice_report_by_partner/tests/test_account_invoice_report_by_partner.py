# -*- coding: utf-8 -*-
# Copyright 2014 Angel Moya <angel.moya@domatix.com>
# Copyright 2017 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase
from odoo import fields


class TestInvoiceReportByPartner(SavepointCase):

    def create_simple_invoice(self):
        date = fields.Date.today()
        return self.env['account.invoice'].create({
            'partner_id': self.partner_id.id,
            'account_id': self.account_id.id,
            'journal_id': self.journal_id,
            'date_invoice': date,
            'invoice_line_ids': [
                (0, 0, {
                    'name': 'test',
                    'account_id': self.account_id.id,
                    'price_unit': 2000.00,
                    'quantity': 1,
                    'product_id': self.product_id.id,
                })],
        })

    @classmethod
    def setUpClass(cls):
        super(TestInvoiceReportByPartner, cls).setUpClass()

        cls.partner_id = cls.env['res.partner'].create({
            'name': 'Test partner',
        })
        cls.product_id = cls.env['product.product'].create({
            'name': 'Test product',
        })
        cls.journal_id = cls.env['account.journal'].search(
            [('type', '=', 'sale')]).id
        cls.account_type = cls.env['account.account.type'].create({
            'name': 'Test account_type'
        })
        cls.account_id = cls.env['account.account'].create({
            'name': 'Test account',
            'code': '440000_demo',
            'user_type_id': cls.account_type.id,
            'reconcile': True})

    def test_report_by_partner(self):
        """Assign report to partner and print invoice"""
        report_obj = self.env['ir.actions.report.xml']

        invoice = self.create_simple_invoice()

        invoice_report = report_obj.search(
            [('report_name', '=', 'account.report_invoice')])

        action_name_copy = 'account.report_invoice_copy'
        invoice_report_copy = invoice_report.copy(
            {'name': 'Invoices copy',
             'report_file': action_name_copy,
             'report_rml': action_name_copy,
             'report_name': action_name_copy})

        self.partner_id.write(
            {'invoice_report_id': invoice_report_copy.id})

        invoice_print = invoice.invoice_print()
        partner_print = invoice.env['report'].get_action(
            invoice, action_name_copy)

        # I check the invoice report
        assert invoice_print == partner_print, \
            'The invoice report is not the partner report'
