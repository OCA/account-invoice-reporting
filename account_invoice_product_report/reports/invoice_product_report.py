# Copyright 2026 Ecosoft Co., Ltd (https://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models


class InvoiceProductReport(models.AbstractModel):
    _name = "report.account_invoice_product_report.invoice_product"
    _description = "Invoice Product Report"

    def _get_report_values(self, docids, data):
        wizard = self.env["invoice.product.report.wizard"].browse(data["wizard_id"])
        products, rows = wizard._get_report_matrix()
        return {
            "doc_ids": wizard.ids,
            "doc_model": "invoice.product.report.wizard",
            "docs": wizard,
            "report_title": "Invoice Product Report",
            "filters": wizard._get_filters(),
            "products": products,
            "rows": rows,
        }
