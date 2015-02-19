# -*- coding: utf-8 -*-

import openerp.tests.common as common
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT


class TestInvoiceReportByPartner(common.TransactionCase):

    def create_simple_invoice(self):
        partner_id = self.ref('base.res_partner_2')
        product_id = self.ref('product.product_product_4')
        today = datetime.now()
        journal_id = self.ref('account.sales_journal')
        date = today.strftime(DEFAULT_SERVER_DATE_FORMAT)
        return self.env['account.invoice']\
            .create({'partner_id': partner_id,
                     'account_id':
                     self.ref('account.a_recv'),
                     'journal_id':
                     journal_id,
                     'date_invoice': date,
                     'invoice_line': [(0, 0, {'name': 'test',
                                              'account_id':
                                              self.ref('account.a_sale'),
                                              'price_unit': 2000.00,
                                              'quantity': 1,
                                              'product_id': product_id,
                                              }
                                       )
                                      ],
                     })

    def setUp(self):
        super(TestInvoiceReportByPartner, self).setUp()

    def test_report_by_partner(self):
        """Assign report to partner and print invoice"""
        report_obj = self.env['ir.actions.report.xml']
        partner_obj = self.env['res.partner']

        invoice = self.create_simple_invoice()

        invoice_report = report_obj.search(
            [('report_name', '=', 'account.report_invoice')])

        action_name_copy = 'account.report_invoice_copy'
        invoice_report_copy = invoice_report.copy(
            {'name': 'Invoices copy',
             'report_file': action_name_copy,
             'report_rml': action_name_copy,
             'report_name': action_name_copy})

        partner_id = self.ref('base.res_partner_2')

        partner = partner_obj.browse(partner_id)

        partner.write(
            {'invoice_report_id': invoice_report_copy.id})

        invoice_print = invoice.invoice_print()
        partner_print = invoice.env['report'].get_action(
            invoice, action_name_copy)

        # I check the invoice report
        assert invoice_print == partner_print, \
            'The invoice report is not the partner report'
