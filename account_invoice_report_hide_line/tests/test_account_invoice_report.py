# Copyright (C) 2019 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import tagged
from odoo.tests.common import Form

from odoo.addons.account.tests.test_account_move_entry import TestAccountMove


@tagged("post_install", "-at_install")
class TestAccountCustomerInvoice(TestAccountMove):
    def test_customer_invoice_show_in_report(self):
        move_form = Form(self.env["account.move"])
        self.account_invoice_line_obj = self.env["account.move.line"]
        self.journalrec = self.env["account.journal"].search([("type", "=", "sale")])[0]
        self.partner3 = self.env.ref("base.res_partner_3")
        move_form.journal_id = self.journalrec
        move_form.partner_id = self.partner3
        with move_form.invoice_line_ids.new() as line_form:
            line_form.product_id = self.env.ref("product.product_product_5")
            line_form.quantity = 10
            line_form.account_id = self.env["account.account"].search(
                [
                    (
                        "user_type_id",
                        "=",
                        self.env.ref("account.data_account_type_revenue").id,
                    ),
                    ("company_id", "=", move_form.company_id.id),
                ],
                limit=1,
            )
            line_form.name = "product 5 test"
            line_form.price_unit = 100.00
        self.invoice = move_form.save()
        invoice_line = self.invoice.invoice_line_ids[0]
        # I check that invoice_line will be checked with show_in_report
        self.assertTrue(
            invoice_line.show_in_report,
            "Fail to show_in_report checked based on Price > 0.0",
        )
        # Update unit price with 0.0
        invoice_line.price_unit = 0.0
        invoice_line._onchange_price_unit()

        # I check that invoice_line will be unchecked with show_in_report
        self.assertFalse(
            invoice_line.show_in_report,
            "Fail to show_in_report unchecked based on Price " "< 0.0",
        )
