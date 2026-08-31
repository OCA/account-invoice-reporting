# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.fields import Command

from odoo.addons.base.tests.common import BaseCommon


class TestUntaxedUnrounded(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env["res.company"].create(
            {
                "name": "test company",
                "currency_id": cls.env.ref("base.JPY").id,
                "country_id": cls.env.ref("base.jp").id,
                "tax_calculation_rounding_method": "round_globally",
            }
        )
        cls.env.company = cls.company
        account_receivable = cls.env["account.account"].create(
            {
                "code": "testrec",
                "name": "receivable",
                "reconcile": True,
                "account_type": "asset_receivable",
            }
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
                "property_account_receivable_id": account_receivable.id,
            }
        )
        cls.product = cls.env["product.product"].create({"name": "Test Product"})
        cls.account_income = cls.env["account.account"].create(
            {"code": "testinc", "name": "income", "account_type": "income"}
        )
        cls.env["account.journal"].create(
            {"code": "test", "name": "test", "type": "sale"}
        )
        cls.tax_group = cls.env["account.tax.group"].create({"name": "Tax Group"})
        cls.tax_10 = cls.env["account.tax"].create(
            {
                "name": "Test Tax 10%",
                "amount": 10.0,
                "type_tax_use": "sale",
                "company_id": cls.company.id,
                "tax_group_id": cls.tax_group.id,
            }
        )
        cls.tax_10_incl = cls.env["account.tax"].create(
            {
                "name": "Test Tax 10% (included)",
                "amount": 10.0,
                "type_tax_use": "sale",
                "company_id": cls.company.id,
                "tax_group_id": cls.tax_group.id,
                "price_include_override": "tax_included",
            }
        )

    def _create_invoice(self, *price_units, tax=None, discount=0.0):
        tax = tax or self.tax_10
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
                                "discount": discount,
                                "tax_ids": [Command.set(tax.ids)],
                            }
                        )
                        for price_unit in price_units
                    ],
                }
            )
        )
        invoice.action_post()
        return invoice

    def test_default_digits_finer_than_jpy(self):
        """The per-company display precision defaults finer than the currency."""
        self.assertEqual(self.company.untaxed_unrounded_digits, 2)
        self.assertEqual(self.company.currency_id.decimal_places, 0)

    def test_line_subtotal_unrounded(self):
        """The line keeps the full-precision subtotal while price_subtotal is
        rounded to the JPY (zero-decimal) currency."""
        invoice = self._create_invoice(100.3)
        line = invoice.invoice_line_ids
        self.assertEqual(line.price_subtotal, 100)
        self.assertAlmostEqual(line.price_subtotal_unrounded, 100.3, places=2)

    def test_amount_untaxed_unrounded_invariant(self):
        """amount_untaxed_unrounded equals the sum of the lines' unrounded
        subtotals, even where the currency-rounded total hides the decimals."""
        invoice = self._create_invoice(100.3, 100.3)
        # Under Round Globally the untaxed total is the global rounding of the
        # exact 200.6 (-> 201 JPY). Note it matches neither the sum of the
        # per-line rounded subtotals (100 + 100 = 200) nor the exact 200.6 --
        # exactly the discrepancy this module discloses.
        self.assertEqual(invoice.amount_untaxed, 201)
        self.assertEqual(sum(invoice.invoice_line_ids.mapped("price_subtotal")), 200)
        self.assertAlmostEqual(invoice.amount_untaxed_unrounded, 200.6, places=2)
        self.assertAlmostEqual(
            invoice.amount_untaxed_unrounded,
            sum(invoice.invoice_line_ids.mapped("price_subtotal_unrounded")),
            places=2,
        )

    def test_price_included_tax_strips_embedded_tax(self):
        """For a price-included tax the unrounded subtotal is the tax-excluded
        base (the price stripped of its embedded tax), not the tax-inclusive
        price_unit. This is the JP consumption-tax case the module targets."""
        invoice = self._create_invoice(110.3, tax=self.tax_10_incl)
        line = invoice.invoice_line_ids
        # Tax-excluded base: 110.3 / 1.1 = 100.2727...; rounded to JPY -> 100.
        self.assertEqual(line.price_subtotal, 100)
        self.assertAlmostEqual(line.price_subtotal_unrounded, 110.3 / 1.1, places=2)
        # It must NOT be the tax-inclusive 110.3 (the bug of the naive formula).
        self.assertNotAlmostEqual(line.price_subtotal_unrounded, 110.3, places=2)
        # And it still reconciles with the document-level unrounded amount.
        self.assertAlmostEqual(
            invoice.amount_untaxed_unrounded,
            line.price_subtotal_unrounded,
            places=2,
        )

    def test_discount_applied_to_unrounded(self):
        """The unrounded subtotal honors the line discount."""
        invoice = self._create_invoice(100.3, discount=10.0)
        line = invoice.invoice_line_ids
        # 100.3 * (1 - 10%) = 90.27; rounded to JPY -> 90.
        self.assertEqual(line.price_subtotal, 90)
        self.assertAlmostEqual(line.price_subtotal_unrounded, 90.27, places=2)

    def test_report_shows_unrounded_at_company_digits(self):
        """The invoice report discloses the unrounded subtotal formatted with
        the company's configured digits (2 -> '100.30'), not the rounded
        '100'."""
        invoice = self._create_invoice(100.3)
        html = (
            self.env["ir.actions.report"]
            ._render_qweb_html("account.report_invoice_with_payments", invoice.ids)[0]
            .decode()
        )
        self.assertIn("100.30", html)
