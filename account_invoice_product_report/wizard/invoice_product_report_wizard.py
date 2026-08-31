# Copyright 2026 Ecosoft Co., Ltd (https://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from collections import defaultdict

from odoo import fields, models


class InvoiceProductReportWizard(models.TransientModel):
    _name = "invoice.product.report.wizard"
    _description = "Invoice Product Report Wizard"

    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)
    customer_ids = fields.Many2many(
        comodel_name="res.partner",
        string="Customers",
        help="Leave empty to include all customers.",
    )
    company_ids = fields.Many2many(
        comodel_name="res.company",
        string="Companies",
        help="Leave empty to include all allowed companies.",
    )

    def _get_domain(self):
        """Build account.move search domain from wizard fields."""
        domain = [
            ("move_type", "in", ["out_invoice", "out_refund"]),
            ("state", "=", "posted"),
            ("invoice_date", ">=", self.date_from),
            ("invoice_date", "<=", self.date_to),
        ]
        if self.company_ids:
            domain.append(("company_id", "in", self.company_ids.ids))
        if self.customer_ids:
            domain.append(("partner_id", "in", self.customer_ids.ids))
        return domain

    def _get_invoices(self):
        """Fetch posted invoices/credit notes matching the wizard filters."""
        return self.env["account.move"].search(
            self._get_domain(), order="partner_id, invoice_date"
        )

    def _get_invoice_lines(self, invoices):
        """Return all product lines for the given invoices via direct search."""
        return self.env["account.move.line"].search(
            [
                ("move_id", "in", invoices.ids),
                ("display_type", "=", "product"),
                ("product_id", "!=", False),
            ]
        )

    def _get_products(self, lines):
        """Return ordered list of unique products found in the invoice lines."""
        return lines.mapped("product_id").sorted(key=lambda p: p.name or "")

    def _get_report_data(self, lines):
        """Net amount matrix keyed by ``(company, partner)``.

        Splitting by company keeps each company's figures separate (no
        cross-company aggregation). Credit notes (out_refund) are subtracted
        from the totals.
        """
        data = {}
        for line in lines:
            move = line.move_id
            company = move.company_id
            partner = move.partner_id
            key = (company.id, partner.id)
            if key not in data:
                data[key] = {
                    "company": company,
                    "partner": partner,
                    "amounts": defaultdict(float),
                }
            sign = -1 if move.move_type == "out_refund" else 1
            data[key]["amounts"][line.product_id.id] += sign * line.price_subtotal
        return sorted(
            data.values(),
            key=lambda r: (r["company"].name or "", r["partner"].name or ""),
        )

    def _get_report_matrix(self):
        """Return ``(products, rows)`` for the customer × product pivot."""
        self.ensure_one()
        lines = self._get_invoice_lines(self._get_invoices())
        return self._get_products(lines), self._get_report_data(lines)

    def _get_filters(self):
        """(label, value) pairs shown at the top of every output."""
        self.ensure_one()
        fmt = "%d-%b-%Y"
        return [
            (
                "From Date",
                self.date_from.strftime(fmt).upper() if self.date_from else "",
            ),
            ("To Date", self.date_to.strftime(fmt).upper() if self.date_to else ""),
            ("Customers", ", ".join(self.customer_ids.mapped("name")) or "All"),
            ("Companies", ", ".join(self.company_ids.mapped("name")) or "All"),
        ]

    def _report_action_prefix(self):
        return "account_invoice_product_report.action_invoice_product_report"

    def _export(self, suffix, **kwargs):
        self.ensure_one()
        action = self.env.ref(f"{self._report_action_prefix()}_{suffix}")
        return action.report_action(self, data={"wizard_id": self.id}, **kwargs)

    def action_export_html(self):
        return self._export("html")

    def action_export_pdf(self):
        return self._export("pdf")

    def action_export_excel(self):
        return self._export("xlsx", config=False)
