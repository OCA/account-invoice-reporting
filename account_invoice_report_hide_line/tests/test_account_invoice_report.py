# Copyright (C) 2019 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.account.tests.account_test_users import AccountTestUsers
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class TestAccountCustomerInvoice(AccountTestUsers):

    def test_customer_invoice_show_in_report(self):
        self.account_invoice_obj = self.env['account.invoice']
        self.journalrec = self.env['account.journal'].search(
            [('type', '=', 'sale')])[0]
        self.partner3 = self.env.ref('base.res_partner_3')
        account_user_type = self.env.ref(
            'account.data_account_type_receivable')
        self.ova = self.env['account.account'].search(
            [('user_type_id',
              '=',
              self.env.ref('account.data_account_type_current_assets').id)],
            limit=1)

        self.account_rec1_id = self.account_model.sudo(
            self.account_manager.id).create(
            dict(code='cust_acc1', name='customer account1',
                 user_type_id=account_user_type.id, reconcile=True))

        invoice_line_data = [(0, 0, {
            'product_id': self.env.ref('product.product_product_5').id,
            'quantity': 10.0, 'account_id': self.env['account.account'].search(
                [('user_type_id', '=',
                  self.env.ref('account.data_account_type_revenue').id)],
                limit=1).id, 'name': 'product test 5',
            'price_unit': 100.00, })]

        self.account_invoice_customer0 = self.account_invoice_obj.sudo(
            self.account_user.id).create(
            dict(name='Test Customer Invoice', journal_id=self.journalrec.id,
                 partner_id=self.partner3.id,
                 account_id=self.account_rec1_id.id,
                 invoice_line_ids=invoice_line_data))

        invoice_line = self.account_invoice_customer0.invoice_line_ids[0]

        # I check that invoice_line will be checked with show_in_report
        self.assertTrue(invoice_line.show_in_report,
                        'Fail to show_in_report checked based on Price > 0.0')

        # Update unit price with 0.0
        invoice_line.price_unit = 0.0
        invoice_line._onchange_price_unit()

        # I check that invoice_line will be unchecked with show_in_report
        self.assertFalse(invoice_line.show_in_report,
                         'Fail to show_in_report unchecked based on Price '
                         '< 0.0')
