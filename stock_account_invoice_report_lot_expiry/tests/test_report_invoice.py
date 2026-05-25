# Copyright 2026 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from datetime import datetime
from unittest.mock import patch

from lxml import html

from odoo import fields
from odoo.tests import Form
from odoo.tests.common import TransactionCase
from odoo.tools import format_date


class TestReportInvoice(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.user.groups_id |= cls.env.ref("stock_account.group_lot_on_invoice")
        cls.partner = cls.env["res.partner"].create({"name": "Test partner"})
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test product",
                "detailed_type": "product",
                "tracking": "lot",
            }
        )
        cls.lot = cls.env["stock.lot"].create(
            {
                "name": "LOT-EXPIRY-001",
                "product_id": cls.product.id,
                "company_id": cls.env.company.id,
                "expiration_date": datetime(2026, 7, 15, 12, 0),
            }
        )

    def _create_invoice(self):
        move_form = Form(
            self.env["account.move"].with_context(default_move_type="out_invoice")
        )
        move_form.partner_id = self.partner
        move_form.invoice_date = fields.Date.from_string("2026-07-01")
        with move_form.invoice_line_ids.new() as line_form:
            line_form.product_id = self.product
            line_form.quantity = 1
            line_form.price_unit = 10.0
        return move_form.save()

    def test_invoice_report_renders_lot_expiry_date(self):
        invoice = self._create_invoice()

        def _get_invoiced_lot_values(move):
            if move != invoice:
                return []
            return [
                {
                    "product_name": self.product.display_name,
                    "quantity": "1.00",
                    "uom_name": self.product.uom_id.name,
                    "lot_name": self.lot.name,
                    "lot_id": self.lot.id,
                }
            ]

        # The method is completed by modules above this one, so we just mimic the shape
        # of the resulting values
        with patch.object(
            self.env.registry["account.move"],
            "_get_invoiced_lot_values",
            _get_invoiced_lot_values,
        ):
            content = html.document_fromstring(
                self.env["ir.actions.report"]._render_qweb_html(
                    "account.account_invoices", invoice.id
                )[0]
            )
        lot_table = html.tostring(
            content.xpath("//table[@name='invoice_snln_table']")[0], encoding="unicode"
        )
        self.assertIn(self.lot.name, lot_table)
        self.assertIn("Expiration Date", lot_table)
        self.assertIn(
            format_date(self.env, fields.Date.to_date(self.lot.expiration_date)),
            lot_table,
        )
