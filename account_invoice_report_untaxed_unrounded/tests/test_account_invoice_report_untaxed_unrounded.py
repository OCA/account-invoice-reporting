# Copyright 2026 Quartile (https://www.quartile.co)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo.fields import Command
from odoo.tests.common import TransactionCase


class TestUntaxedUnrounded(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env["res.company"].create(
            {
                "name": "test company",
                "currency_id": cls.env.ref("base.JPY").id,
                "tax_calculation_rounding_method": "round_globally",
            }
        )
        cls.env.company = cls.company
        cls.partner = cls.env["res.partner"].create({"name": "Test Partner"})
        cls.product = cls.env["product.product"].create({"name": "Test Product"})
        cls.account_income = cls.env["account.account"].create(
            {"code": "test_inc", "name": "income", "account_type": "income"}
        )
        cls.tax_10 = cls.env["account.tax"].create(
            {
                "name": "Test Tax 10%",
                "amount": 10.0,
                "type_tax_use": "sale",
                "company_id": cls.company.id,
            }
        )

    def _create_invoice(self, price_unit):
        invoice = (
            self.env["account.move"]
            .with_company(self.company)
            .create(
                {
                    "move_type": "out_invoice",
                    "partner_id": self.partner.id,
                    "currency_id": self.company.currency_id.id,
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "product_id": self.product.id,
                                "account_id": self.account_income.id,
                                "quantity": 1,
                                "price_unit": price_unit,
                                "tax_ids": [Command.set(self.tax_10.ids)],
                            }
                        )
                    ],
                }
            )
        )
        invoice.action_post()
        return invoice

    def test_subtotal_rounded(self):
        """A line whose subtotal loses decimals is flagged and exposes the
        unrounded amount."""
        invoice = self._create_invoice(100.3)
        line = invoice.invoice_line_ids
        # price_subtotal is rounded to JPY (zero decimals).
        self.assertEqual(line.price_subtotal, 100)
        self.assertTrue(line.is_price_subtotal_rounded)
        self.assertAlmostEqual(line.price_subtotal_unrounded, 100.3, places=2)

    def test_subtotal_not_rounded(self):
        """A line with no rounding difference keeps the standard
        presentation."""
        invoice = self._create_invoice(100)
        line = invoice.invoice_line_ids
        self.assertEqual(line.price_subtotal, 100)
        self.assertFalse(line.is_price_subtotal_rounded)
        self.assertAlmostEqual(line.price_subtotal_unrounded, 100, places=2)
