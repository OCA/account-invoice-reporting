# Copyright 2026 Ecosoft Co., Ltd (https://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import Command, fields
from odoo.tests import Form, tagged
from odoo.tests.common import TransactionCase

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


class TestInvoiceProductReportWizard(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.wizard_model = cls.env["invoice.product.report.wizard"]
        cls.move_model = cls.env["account.move"]
        # Configure a document layout so the View / PDF report actions return
        # the report directly instead of the "Configure Layout" act_window.
        cls.env.company.external_report_layout_id = cls.env.ref(
            "web.external_layout_standard"
        )

        cls.account_revenue = cls.env["account.account"].search(
            [
                ("account_type", "=", "income"),
                ("company_ids", "=", cls.env.company.id),
            ],
            limit=1,
        )
        cls.partner_a = cls.env["res.partner"].create(
            {"name": "Partner A", "ref": "CUST-001", "customer_rank": 1}
        )
        cls.partner_b = cls.env["res.partner"].create(
            {"name": "Partner B", "ref": "CUST-002", "customer_rank": 1}
        )
        cls.product_1 = cls.env["product.product"].create(
            {"name": "Product Alpha", "type": "service"}
        )
        cls.product_2 = cls.env["product.product"].create(
            {"name": "Product Beta", "type": "service"}
        )
        cls.date_from = fields.Date.from_string("2026-01-01")
        cls.date_to = fields.Date.from_string("2026-01-31")

    def _create_invoice(
        self, partner, lines, move_type="out_invoice", date="2026-01-15"
    ):
        """Helper: create and post an invoice."""
        invoice = self.move_model.create(
            {
                "move_type": move_type,
                "partner_id": partner.id,
                "invoice_date": date,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "product_id": product.id,
                            "quantity": 1,
                            "price_unit": amount,
                            "account_id": self.account_revenue.id,
                        }
                    )
                    for product, amount in lines
                ],
            }
        )
        invoice.action_post()
        return invoice

    def _make_wizard(self, date_from=None, date_to=None, customers=None):
        return self.wizard_model.create(
            {
                "date_from": date_from or self.date_from,
                "date_to": date_to or self.date_to,
                "customer_ids": [Command.set(customers or [])],
                "company_ids": [Command.set([self.env.company.id])],
            }
        )

    # ── Tests ────────────────────────────────────────────────────────────────────

    def test_1_export_actions_return_report_actions(self):
        """The View / PDF / Excel buttons each return an ir.actions.report."""
        wizard = self._make_wizard()
        cases = [
            (
                wizard.action_export_html,
                "account_invoice_product_report.invoice_product",
            ),
            (
                wizard.action_export_pdf,
                "account_invoice_product_report.invoice_product",
            ),
            (
                wizard.action_export_excel,
                "account_invoice_product_report.invoice_product_xlsx",
            ),
        ]
        for method, report_name in cases:
            action = method()
            self.assertEqual(action.get("type"), "ir.actions.report")
            self.assertEqual(action.get("report_name"), report_name)

    def test_2_get_invoices_respects_date_range(self):
        """Only invoices within date_from–date_to are returned."""
        self._create_invoice(self.partner_a, [(self.product_1, 100)], date="2026-01-15")
        self._create_invoice(self.partner_a, [(self.product_1, 200)], date="2026-02-01")

        wizard = self._make_wizard()
        invoices = wizard._get_invoices()
        dates = invoices.mapped("invoice_date")
        self.assertTrue(all(self.date_from <= d <= self.date_to for d in dates))

    def test_3_get_invoice_lines_returns_product_lines_only(self):
        """_get_invoice_lines returns only product display_type lines."""
        invoice = self._create_invoice(
            self.partner_a, [(self.product_1, 100), (self.product_2, 200)]
        )
        wizard = self._make_wizard()
        lines = wizard._get_invoice_lines(invoice)
        self.assertTrue(all(ln.display_type == "product" for ln in lines))
        self.assertTrue(all(ln.product_id for ln in lines))
        self.assertEqual(len(lines), 2)

    def test_4_get_products_returns_unique_sorted(self):
        """_get_products returns unique products sorted by name."""
        inv1 = self._create_invoice(self.partner_a, [(self.product_1, 100)])
        inv2 = self._create_invoice(
            self.partner_b, [(self.product_1, 50), (self.product_2, 75)]
        )
        wizard = self._make_wizard()
        lines = wizard._get_invoice_lines(inv1 | inv2)
        products = wizard._get_products(lines)
        self.assertEqual(len(products), 2)
        names = [p.name for p in products]
        self.assertEqual(names, sorted(names))

    def test_5_report_data_sums_multiple_invoices(self):
        """Amounts from multiple invoices for the same partner+product are summed."""
        self._create_invoice(self.partner_a, [(self.product_1, 100)])
        self._create_invoice(self.partner_a, [(self.product_1, 200)])
        wizard = self._make_wizard()
        invoices = wizard._get_invoices()
        lines = wizard._get_invoice_lines(invoices)
        report_data = wizard._get_report_data(lines)

        partner_row = next(
            r for r in report_data if r["partner"].id == self.partner_a.id
        )
        total = partner_row["amounts"].get(self.product_1.id, 0.0)
        self.assertAlmostEqual(total, 300.0)

    def test_6_report_data_subtracts_credit_notes(self):
        """Credit notes (out_refund) are subtracted from invoice totals."""
        self._create_invoice(self.partner_a, [(self.product_1, 500)])
        self._create_invoice(
            self.partner_a, [(self.product_1, 150)], move_type="out_refund"
        )
        wizard = self._make_wizard()
        invoices = wizard._get_invoices()
        lines = wizard._get_invoice_lines(invoices)
        report_data = wizard._get_report_data(lines)

        partner_row = next(
            r for r in report_data if r["partner"].id == self.partner_a.id
        )
        total = partner_row["amounts"].get(self.product_1.id, 0.0)
        self.assertAlmostEqual(total, 350.0)

    def test_7_filter_by_customer(self):
        """customer_ids filter limits invoices to selected partners."""
        self._create_invoice(self.partner_a, [(self.product_1, 100)])
        self._create_invoice(self.partner_b, [(self.product_2, 200)])
        wizard = self._make_wizard(customers=[self.partner_a.id])
        invoices = wizard._get_invoices()
        self.assertTrue(all(inv.partner_id == self.partner_a for inv in invoices))

    def test_8_reports_render(self):
        """The XLSX and HTML outputs render to valid content for the data."""
        self._create_invoice(self.partner_a, [(self.product_1, 100)])
        self._create_invoice(self.partner_b, [(self.product_2, 200)])
        wizard = self._make_wizard()
        data = {"wizard_id": wizard.id}
        report = self.env["ir.actions.report"]

        xlsx = report._render_xlsx(
            "account_invoice_product_report.action_invoice_product_report_xlsx",
            wizard.ids,
            data,
        )[0]
        self.assertEqual(xlsx[:2], b"PK")  # valid .xlsx (zip) magic

        html = report._render_qweb_html(
            "account_invoice_product_report.action_invoice_product_report_html",
            wizard.ids,
            data,
        )[0]
        self.assertIn(b"Product Alpha", html)  # product column header present


@tagged("post_install", "-at_install")
class TestInvoiceProductReportMultiCompany(AccountTestInvoicingCommon):
    """Multi-company: same customer + product across companies must not merge."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company_a = cls.company_data["company"]
        cls.company_data_2 = cls.setup_other_company()
        cls.company_b = cls.company_data_2["company"]

    def _make_wizard(self):
        return (
            self.env["invoice.product.report.wizard"]
            .with_context(allowed_company_ids=[self.company_a.id, self.company_b.id])
            .create(
                {
                    "date_from": "2026-01-01",
                    "date_to": "2026-01-31",
                    "company_ids": [
                        Command.set([self.company_a.id, self.company_b.id])
                    ],
                }
            )
        )

    def _post_invoice(self, company, partner, product, price):
        """Post a 1-line customer invoice in ``company`` (Form derives accounts)."""
        move_form = Form(
            self.env["account.move"]
            .with_company(company)
            .with_context(default_move_type="out_invoice")
        )
        move_form.invoice_date = fields.Date.from_string("2026-01-15")
        move_form.partner_id = partner
        with move_form.invoice_line_ids.new() as line:
            line.product_id = product
            line.price_unit = price
        move = move_form.save()
        move.action_post()
        return move

    def test_same_customer_product_split_by_company(self):
        # Same partner + product invoiced in both companies, different amounts.
        self._post_invoice(self.company_a, self.partner_a, self.product_a, 100)
        self._post_invoice(self.company_b, self.partner_a, self.product_a, 250)
        wizard = self._make_wizard()
        rows = wizard._get_report_data(
            wizard._get_invoice_lines(wizard._get_invoices())
        )

        rows_a = [r for r in rows if r["company"] == self.company_a]
        rows_b = [r for r in rows if r["company"] == self.company_b]
        # One row per company — NOT merged into a single 350 row.
        self.assertEqual(len(rows_a), 1)
        self.assertEqual(len(rows_b), 1)
        self.assertAlmostEqual(rows_a[0]["amounts"][self.product_a.id], 100)
        self.assertAlmostEqual(rows_b[0]["amounts"][self.product_a.id], 250)
