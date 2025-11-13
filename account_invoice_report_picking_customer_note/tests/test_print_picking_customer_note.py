# Copyright 2025 Moduon Team S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import fields
from odoo.tests import Form, TransactionCase


class TestSaleStockPickingNote(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Mr. Odoo",
                "picking_customer_note": "Test customer note",
            }
        )

    def _create_invoice(self):
        invoice_vals = [
            (
                0,
                0,
                {
                    "product_id": False,
                    "quantity": 1.0,
                    "name": "Line 1",
                    "price_unit": 200.00,
                },
            )
        ]
        invoice = (
            self.env["account.move"]
            .with_context(check_move_validity=False)
            .create(
                {
                    "journal_id": self.env["account.journal"]
                    .search([("type", "=", "sale")], limit=1)
                    .id,
                    "partner_id": self.partner.id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": invoice_vals,
                }
            )
        )
        return invoice

    def _create_sale_order(self):
        product = self.env["product.product"].create(
            {
                "name": "test_product",
                "type": "product",
                "standard_price": 1.0,
                "list_price": 1.0,
            }
        )
        so_vals = {
            "partner_id": self.partner.id,
            "date_order": fields.Datetime.now(),
            "order_line": [
                (
                    0,
                    0,
                    {
                        "name": product.name,
                        "product_id": product.id,
                        "price_unit": product.list_price,
                    },
                )
            ],
        }
        return self.env["sale.order"].create(so_vals)

    def test_print_picking_customer_note_in_invoice(self):
        invoice_form = Form(self._create_invoice())
        invoice = invoice_form.save()
        invoice.action_post()
        report = self.env.ref("account.account_invoices_without_payment")
        res = str(
            report._render_qweb_html(
                "account.account_invoices_without_payment", invoice.id
            )[0]
        )
        self.assertRegex(res, self.partner.picking_customer_note)

    def test_print_picking_customer_note_in_invoice_from_sale_order(self):
        picking_customer_note = "Test comment"
        product = self.env["product.product"].create(
            {
                "name": "test_product",
                "type": "product",
                "standard_price": 1.0,
                "list_price": 1.0,
            }
        )
        so_vals = {
            "partner_id": self.partner.id,
            "date_order": fields.Datetime.now(),
            "order_line": [
                (
                    0,
                    0,
                    {
                        "name": product.name,
                        "product_id": product.id,
                        "price_unit": product.list_price,
                    },
                )
            ],
        }
        so = self.env["sale.order"].create(so_vals)
        so.picking_customer_note = picking_customer_note
        so.action_confirm()
        invoice = so._create_invoices()
        invoice.action_post()
        report = self.env.ref("account.account_invoices_without_payment")
        res = str(
            report._render_qweb_html(
                "account.account_invoices_without_payment", invoice.id
            )[0]
        )
        self.assertRegex(res, picking_customer_note)

        def test_print_picking_customer_note_in_invoice_more_one_sale_orders(self):
            invoice = self._create_invoice()
            so_1 = self._create_sale_order()
            so_2 = self._create_sale_order()
            so_1.picking_customer_note = "Picking Note"
            so_2.picking_customer_note = "Picking Note SO 2"
            invoice.invoice_line_ids.sale_line_ids.order_id = [so_1, so_2]
            invoice.action_post()
            report = self.env.ref("account.account_invoices_without_payment")
            res = str(
                report._render_qweb_html(
                    "account.account_invoices_without_payment", invoice.id
                )[0]
            )
            self.assertRegex(res, self.partner.picking_customer_note)
