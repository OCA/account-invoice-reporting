# Copyright 2026 Moduon Team S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests import Form, tagged

# ruff: noqa: E501
from odoo.addons.stock_picking_invoice_link.tests.test_stock_picking_invoice_link import (
    TestStockPickingInvoiceLink,
)


@tagged("post_install", "-at_install")
class TestAccountInvoiceReportStockPackaging(TestStockPickingInvoiceLink):
    @classmethod
    def _create_stock_picking_and_confirm(cls):
        """Overwrite entirely to set packaging on moves"""
        cls.packaging_a = cls.env["product.packaging"].create(
            {
                "name": "Box",
                "product_id": cls.product_a.id,
                "qty": 2,
            }
        )
        picking_form = Form(
            cls.env["stock.picking"].with_context(
                default_picking_type_id=cls.picking_type_out.id,
                default_partner_id=cls.partner_a.id,
            )
        )
        for product in cls.product_a + cls.product_b + cls.product_c:
            with picking_form.move_ids_without_package.new() as line_form:
                line_form.product_id = product
                line_form.product_uom_qty = 2
        picking = picking_form.save()
        picking.action_assign()
        picking.move_line_ids.write({"quantity": 2})
        # Write packaging information
        picking.move_line_ids.filtered_domain(
            [("product_id", "=", cls.product_a.id)]
        ).move_id.write(
            {
                "product_packaging_id": cls.packaging_a.id,
                "product_packaging_quantity": 1.1,
            }
        )
        picking.button_validate()
        return picking

    def test_account_move_line_packaging_info(self):
        """Test _get_packaging_info returns correct packaging string"""
        invoice_line = self.invoiceA.invoice_line_ids.filtered_domain(
            [("product_id", "=", self.product_a.id)]
        )
        self.assertTrue(invoice_line.move_line_ids)
        self.assertTrue(invoice_line.move_line_ids.mapped("product_packaging_id"))
        self.assertIn("1.1 Box", invoice_line._get_packaging_info())

    def test_account_move_line_without_packaging_info(self):
        """Test _get_packaging_info returns empty string when no packaging"""
        invoice_line = self.invoiceA.invoice_line_ids.filtered_domain(
            [("product_id", "=", self.product_b.id)]
        )
        self.assertTrue(invoice_line.move_line_ids)
        self.assertEqual(invoice_line._get_packaging_info(), "")
