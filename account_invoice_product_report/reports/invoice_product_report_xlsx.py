# Copyright 2026 Ecosoft Co., Ltd (https://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models

from odoo.addons.report_xlsx_helper.report.report_xlsx_format import (
    FORMATS,
    XLS_HEADERS,
)


class InvoiceProductReportXlsx(models.AbstractModel):
    _name = "report.account_invoice_product_report.invoice_product_xlsx"
    _inherit = "report.report_xlsx.abstract"
    _description = "Invoice Product Report XLSX"

    def _resolve_wizard(self, objects, data):
        if data and data.get("wizard_id"):
            return self.env["invoice.product.report.wizard"].browse(data["wizard_id"])
        return objects

    def _get_col_specs(self, products):
        col_specs = {
            "000_company": {
                "header": {"value": "Company"},
                "data": {"value": self._render("company.name or ' '")},
                "width": 24,
                "format": FORMATS["format_tcell_left"],
            },
            "001_code": {
                "header": {"value": "Customer Code"},
                "data": {"value": self._render("partner.ref or ' '")},
                "width": 16,
                "format": FORMATS["format_tcell_left"],
            },
            "002_name": {
                "header": {"value": "Customer Name"},
                "data": {"value": self._render("partner.name or ' '")},
                "width": 30,
            },
        }
        for index, product in enumerate(products):
            col_specs["%03d_p%d" % (index + 3, product.id)] = {
                "header": {"value": product.name or ""},
                "data": {
                    "value": self._render("amounts.get(%d, 0.0)" % product.id),
                    "type": "number",
                    "format": FORMATS["format_tcell_amount_right"],
                },
                "width": max(len(product.name or "") + 2, 14),
            }
        return col_specs

    def _get_ws_params(self, workbook, data, objects):
        wizard = self._resolve_wizard(objects, data)
        products, _rows = wizard._get_report_matrix()
        col_specs = self._get_col_specs(products)
        return [
            {
                "ws_name": "Invoice Product Report",
                "generate_ws_method": "_report_content",
                "title": "Invoice Product Report",
                "wanted_list": sorted(col_specs),
                "col_specs": col_specs,
            }
        ]

    def _write_filters(self, ws, row, wizard):
        for label, value in wizard._get_filters():
            ws.write(row, 0, label, FORMATS["format_left_bold"])
            ws.write(row, 1, value or "", FORMATS["format_left"])
            row += 1
        return row

    def _report_content(self, workbook, ws, ws_params, data, objects):
        wizard = self._resolve_wizard(objects, data)
        products, rows = wizard._get_report_matrix()

        ws.set_landscape()
        ws.set_header(XLS_HEADERS["xls_headers"]["standard"])
        ws.set_footer(XLS_HEADERS["xls_footers"]["standard"])
        self._set_column_width(ws, ws_params)

        row = self._write_ws_title(ws, 0, ws_params, merge_range=True)
        row = self._write_filters(ws, row, wizard)
        row += 1

        row = self._write_line(
            ws,
            row,
            ws_params,
            col_specs_section="header",
            default_format=FORMATS["format_theader_blue_center"],
        )
        ws.freeze_panes(row, 0)

        for line in rows:
            row = self._write_line(
                ws,
                row,
                ws_params,
                col_specs_section="data",
                render_space={
                    "company": line["company"],
                    "partner": line["partner"],
                    "amounts": line["amounts"],
                },
                default_format=FORMATS["format_tcell_left"],
            )
        return row
