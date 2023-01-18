# Copyright 2011 Domsense s.r.l. <http://www.domsense.com>
# Copyright 2013 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
# Copyright 2017 Tecnativa - Vicent Cubells
# Copyright 2018 Alex Comba <alex.comba@agilebg.com>
# Copyright 2020 Tecnativa - João Marques
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import Form
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestProdLot(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_company = cls.env.user.company_id
        cls.partner = cls.env["res.partner"].create(
            {"name": "Test partner", "lang": "en_US"}
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Product Test",
                "detailed_type": "product",
                "tracking": "lot",
                "invoice_policy": "delivery",
                "list_price": 15,
            }
        )
        cls.product2 = cls.env["product.product"].create(
            {
                "name": "Product Test 2",
                "detailed_type": "product",
                "tracking": "serial",
                "invoice_policy": "delivery",
                "list_price": 10,
            }
        )
        order_form = Form(cls.env["sale.order"])
        order_form.partner_id = cls.partner
        with order_form.order_line.new() as line_form:
            line_form.product_id = cls.product
            line_form.product_uom_qty = 4
        with order_form.order_line.new() as line_form:
            line_form.product_id = cls.product2
            line_form.product_uom_qty = 1
        cls.sale = order_form.save()
        cls.lot1 = cls.env["stock.production.lot"].create(
            {
                "name": "Lot 1",
                "product_id": cls.product.id,
                "company_id": cls.user_company.id,
            }
        )
        cls.lot2 = cls.env["stock.production.lot"].create(
            {
                "name": "Lot 2",
                "product_id": cls.product.id,
                "company_id": cls.user_company.id,
            }
        )
        cls.serial = cls.env["stock.production.lot"].create(
            {
                "name": "Serial 1",
                "product_id": cls.product2.id,
                "company_id": cls.user_company.id,
            }
        )

    def qty_on_hand(self, product, quantity, lot):
        """Update Product quantity."""
        res = product.action_update_quantity_on_hand()
        stock_quant_form = Form(
            self.env["stock.quant"].with_context(**res["context"]),
            view="stock.view_stock_quant_tree_inventory_editable",
        )
        stock_quant_form.inventory_quantity = quantity
        stock_quant_form.lot_id = lot
        quant = stock_quant_form.save()
        quant.action_apply_inventory()

    def test_00_sale_stock_invoice_product_lot(self):
        # update quantities with their related lots
        self.qty_on_hand(self.product, 2, self.lot1)
        self.qty_on_hand(self.product, 2, self.lot2)
        self.qty_on_hand(self.product2, 1, self.serial)
        # confirm quotation
        self.sale.action_confirm()
        picking = self.sale.picking_ids[:1]
        picking.action_confirm()
        picking.action_assign()
        for sml in picking.move_lines.mapped("move_line_ids"):
            sml.qty_done = sml.product_qty
        picking._action_done()
        # create invoice
        invoice = self.sale._create_invoices()
        self.assertEqual(len(invoice.invoice_line_ids), 2)
        line = invoice.invoice_line_ids.filtered(
            lambda x: x.product_id.id == self.product.id
        )
        # We must have two lots
        self.assertEqual(len(line.prod_lot_ids.ids), 2)
        self.assertIn("Lot 1", line.lots_grouped_by_quantity())
        self.assertIn("Lot 2", line.lots_grouped_by_quantity())
        # check if quantity is displayed in lots_grouped_by_quantity()
        self.assertEqual(2.0, line.lots_grouped_by_quantity()["Lot 1"])

    def test_01_sale_stock_delivery_partial_invoice_product_lot(self):
        # update quantities with their related lots
        self.qty_on_hand(self.product, 3, self.lot1)
        self.qty_on_hand(self.product, 3, self.lot2)
        # confirm quotation
        self.sale.action_confirm()
        picking = self.sale.picking_ids[:1]
        picking.action_confirm()
        picking.action_assign()
        # deliver partially only one lot
        picking.move_lines[0].move_line_ids[0].write({"qty_done": 2.0})
        backorder_wizard_dict = picking.button_validate()
        backorder_wiz = Form(
            self.env[backorder_wizard_dict["res_model"]].with_context(
                **backorder_wizard_dict["context"]
            )
        ).save()
        backorder_wiz.process()
        # create invoice
        invoice = self.sale._create_invoices()
        self.assertEqual(len(invoice.invoice_line_ids), 1)
        line = invoice.invoice_line_ids
        # We must have only one lot
        self.assertEqual(len(line.prod_lot_ids.ids), 1)
        self.assertEqual(line.prod_lot_ids.id, self.lot1.id)
        self.assertIn("Lot 1", line.lots_grouped_by_quantity())
        self.assertNotIn("Lot 2", line.lots_grouped_by_quantity())
        # check if quantity is displayed in lots_grouped_by_quantity()
        self.assertEqual(2.0, line.lots_grouped_by_quantity()["Lot 1"])

    def test_02_sale_stock_delivery_partial_invoice_product_lot(self):
        # update quantities with their related lots
        self.qty_on_hand(self.product, 3, self.lot1)
        self.qty_on_hand(self.product, 3, self.lot2)
        # confirm quotation
        self.sale.action_confirm()
        picking = self.sale.picking_ids[:1]
        picking.action_confirm()
        picking.action_assign()
        # deliver partially both lots
        picking.move_lines[0].move_line_ids[0].write({"qty_done": 1.0})
        picking.move_lines[0].move_line_ids[1].write({"qty_done": 1.0})
        backorder_wizard_dict = picking.button_validate()
        backorder_wiz = Form(
            self.env[backorder_wizard_dict["res_model"]].with_context(
                **backorder_wizard_dict["context"]
            )
        ).save()
        backorder_wiz.process()
        # create invoice
        invoice = self.sale._create_invoices()
        self.assertEqual(len(invoice.invoice_line_ids), 1)
        line = invoice.invoice_line_ids
        # We must have two lots
        self.assertEqual(len(line.prod_lot_ids.ids), 2)
        self.assertIn(self.lot1.id, line.prod_lot_ids.ids)
        self.assertIn(self.lot2.id, line.prod_lot_ids.ids)
        self.assertIn("Lot 1", line.lots_grouped_by_quantity())
        self.assertIn("Lot 2", line.lots_grouped_by_quantity())
        # check if both quantities are displayed in lots_grouped_by_quantity()
        self.assertEqual(1.0, line.lots_grouped_by_quantity()["Lot 1"])
        self.assertNotEqual(2.0, line.lots_grouped_by_quantity()["Lot 2"])
