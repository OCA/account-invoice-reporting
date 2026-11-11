# Copyright 2020 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta

from freezegun import freeze_time

from odoo.tests import Form

from odoo.addons.base.tests.common import BaseCommon


class TestReportGroupedSaleMrp(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mrp_bom = cls.env["mrp.bom"]
        cls.partner = cls.env["res.partner"].create({"name": "Customer test"})
        # create a kit (kit_1) with 2 components
        cls.product_kit_1 = cls.env["product.product"].create(
            {"name": "Product Kit 1", "type": "consu"}
        )
        cls.component_1_kit_1 = cls.env["product.product"].create(
            {"name": "Component 1 Kit 1", "type": "product"}
        )
        cls.component_2_kit_1 = cls.env["product.product"].create(
            {"name": "Component 2 Kit 1", "type": "product"}
        )
        bom_form = Form(cls.mrp_bom)
        bom_form.product_tmpl_id = cls.product_kit_1.product_tmpl_id
        bom_form.product_id = cls.product_kit_1
        bom_form.type = "phantom"
        with bom_form.bom_line_ids.new() as line:
            line.product_id = cls.component_1_kit_1
        with bom_form.bom_line_ids.new() as line:
            line.product_id = cls.component_2_kit_1
        cls.bom_kit_1 = bom_form.save()
        # create another kit (kit_2) with: 2 components + kit_1
        cls.product_kit_2 = cls.env["product.product"].create(
            {"name": "Product Kit 2", "type": "consu"}
        )
        cls.component_1_kit_2 = cls.env["product.product"].create(
            {"name": "Component 1 Kit 2", "type": "product"}
        )
        cls.component_2_kit_2 = cls.env["product.product"].create(
            {"name": "Component 2 Kit 2", "type": "product"}
        )
        bom_form = Form(cls.mrp_bom)
        bom_form.product_tmpl_id = cls.product_kit_2.product_tmpl_id
        bom_form.product_id = cls.product_kit_2
        bom_form.type = "phantom"
        with bom_form.bom_line_ids.new() as line:
            line.product_id = cls.component_1_kit_2
        with bom_form.bom_line_ids.new() as line:
            line.product_id = cls.component_2_kit_2
        with bom_form.bom_line_ids.new() as line:
            line.product_id = cls.product_kit_1
        cls.bom_kit_2 = bom_form.save()
        # create a manufactured product (normal BoM, not a kit) with 1
        # component of qty 2, so that dividing its quantity as for a kit
        # would change it
        cls.product_manufactured = cls.env["product.product"].create(
            {"name": "Product Manufactured", "type": "product"}
        )
        cls.component_manufactured = cls.env["product.product"].create(
            {"name": "Component Manufactured", "type": "product"}
        )
        bom_form = Form(cls.mrp_bom)
        bom_form.product_tmpl_id = cls.product_manufactured.product_tmpl_id
        bom_form.product_id = cls.product_manufactured
        bom_form.type = "normal"
        with bom_form.bom_line_ids.new() as line:
            line.product_id = cls.component_manufactured
            line.product_qty = 2
        cls.bom_manufactured = bom_form.save()
        # create a sales order
        sale_form = Form(cls.env["sale.order"])
        sale_form.partner_id = cls.partner
        with sale_form.order_line.new() as line_form:
            line_form.product_id = cls.product_kit_2
            line_form.product_uom_qty = 2
        cls.sale_order = sale_form.save()
        # Avoid problems when `delivery` module is installed
        if "carrier_id" in cls.sale_order._fields:
            cls.sale_order["carrier_id"] = False

    def test_account_invoice_group_picking(self):
        # confirm quotation
        # with freeze_time is used so the account.move lines_grouped_by_picking
        # method sorts lines as expected
        with freeze_time(datetime.now() - timedelta(seconds=5)):
            self.sale_order.action_confirm()
            self.assertEqual(len(self.sale_order.picking_ids), 1)
            picking_1 = self.sale_order.picking_ids
            self.assertEqual(len(picking_1.move_ids), 4)
            self.assertEqual(self.sale_order.order_line.move_ids, picking_1.move_ids)
            # deliver the sold kit_2 components
            picking_1.action_confirm()
            picking_1.mapped("move_ids").write({"quantity": 2})
            picking_1.button_validate()

        # Change the existing order line qty from 2 to 3 and deliver
        # the new kit_2
        with Form(self.sale_order) as sale_form:
            with sale_form.order_line.edit(0) as line_form:
                line_form.product_uom_qty = 3
        self.assertEqual(len(self.sale_order.picking_ids), 2)
        picking_2 = self.sale_order.picking_ids - picking_1
        self.assertEqual(len(picking_2.move_ids), 4)
        self.assertEqual(
            self.sale_order.order_line.move_ids,
            picking_1.move_ids + picking_2.move_ids,
        )
        picking_2.action_confirm()
        picking_2.mapped("move_ids").write({"quantity": 1})
        picking_2.button_validate()
        # Test directly grouping method
        move = self.sale_order._create_invoices()
        groups = move.lines_grouped_by_picking()
        self.assertEqual(len(groups), 2)
        self.assertDictEqual(
            groups[0],
            {"line": move.invoice_line_ids, "picking": picking_1, "quantity": 2.0},
        )
        self.assertDictEqual(
            groups[1],
            {"line": move.invoice_line_ids, "picking": picking_2, "quantity": 1.0},
        )

    def test_account_invoice_group_picking_normal_bom(self):
        # add the manufactured product to the sales order of kit_2
        kit_sale_line = self.sale_order.order_line
        with Form(self.sale_order) as sale_form:
            with sale_form.order_line.new() as line_form:
                line_form.product_id = self.product_manufactured
                line_form.product_uom_qty = 2
        manufactured_sale_line = self.sale_order.order_line - kit_sale_line
        self.sale_order.action_confirm()
        self.assertEqual(len(self.sale_order.picking_ids), 1)
        picking = self.sale_order.picking_ids
        # deliver the sold kit_2 components and the manufactured product
        picking.mapped("move_ids").write({"quantity": 2})
        picking.button_validate()
        # Test directly grouping method
        move = self.sale_order._create_invoices()
        groups = move.lines_grouped_by_picking()
        self.assertEqual(len(groups), 2)
        self.assertDictEqual(
            groups[0],
            {"line": kit_sale_line.invoice_lines, "picking": picking, "quantity": 2.0},
        )
        self.assertDictEqual(
            groups[1],
            {
                "line": manufactured_sale_line.invoice_lines,
                "picking": picking,
                "quantity": 2.0,
            },
        )
