# -*- coding: utf-8 -*-
# Copyright 2011 Domsense s.r.l. <http://www.domsense.com>
# Copyright 2013 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
# Copyright 2017 Vicent Cubells <vicent.cubells@tecnativa.com>
# Copyright 2018 Alex Comba <alex.comba@agilebg.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common
from odoo.tools.misc import formatLang


class TestProdLot(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestProdLot, cls).setUpClass()
        cls.partner = cls.env['res.partner'].create({
            'name': 'Test partner',
        })
        cls.product = cls.env['product.product'].create({
            'name': 'Product Test',
            'type': 'product',
            'tracking': 'lot',
            'invoice_policy': 'delivery',
        })
        cls.sale = cls.env['sale.order'].create({
            'partner_id': cls.partner.id,
            'partner_invoice_id': cls.partner.id,
            'partner_shipping_id': cls.partner.id,
            'order_line': [(0, 0, {
                'name': cls.product.name,
                'product_id': cls.product.id,
                'product_uom_qty': 4,
                'product_uom': cls.product.uom_id.id,
                'price_unit': 15.0,
            })],
        })
        cls.lot1 = cls.env['stock.production.lot'].create({
            'name': 'Lot 1',
            'product_id': cls.product.id,
        })
        cls.lot2 = cls.env['stock.production.lot'].create({
            'name': 'Lot 2',
            'product_id': cls.product.id,
        })
        cls.stock_location = cls.env.ref('stock.stock_location_stock')
        cls.customer_location = cls.env.ref('stock.stock_location_customers')
        cls.picking_type_out = cls.env.ref('stock.picking_type_out')

    def qty_on_hand(self, product, location, quantity, lot):
        """Update Product quantity."""
        wiz = self.env['stock.change.product.qty'].create({
            'location_id': location.id,
            'product_id': product.id,
            'new_quantity': quantity,
            'lot_id': lot.id,
        })
        wiz.change_product_qty()

    def test_00_sale_stock_invoice_product_lot(self):
        # confirm quotation
        self.sale.action_confirm()
        picking = self.sale.picking_ids[:1]
        # set lots and transfer
        picking.action_confirm()
        picking.action_assign()
        picking.do_prepare_partial()
        qty_lot = 2.0
        self.env['stock.pack.operation'].create({
            'product_id': self.product.id,
            'product_qty': 2,
            'product_uom_id': self.product.uom_id.id,
            'location_id': self.stock_location.id,
            'location_dest_id': self.customer_location.id,
            'picking_id': picking.id,
            'pack_lot_ids': [(0, 0, {'lot_id': self.lot1.id, 'qty': qty_lot})],
        })
        self.env['stock.pack.operation'].create({
            'product_id': self.product.id,
            'product_qty': 2,
            'product_uom_id': self.product.uom_id.id,
            'location_id': self.stock_location.id,
            'location_dest_id': self.customer_location.id,
            'picking_id': picking.id,
            'pack_lot_ids': [(0, 0, {'lot_id': self.lot2.id, 'qty': qty_lot})],
        })
        picking.do_transfer()
        # create invoice
        inv_id = self.sale.action_invoice_create()
        invoice = self.env['account.invoice'].browse(inv_id)
        self.assertEqual(len(invoice.invoice_line_ids), 1)
        line = invoice.invoice_line_ids
        # We must have two lots
        self.assertEqual(len(line.prod_lot_ids.ids), 2)
        self.assertIn('Lot 1', line.lot_formatted_note)
        self.assertIn('Lot 2', line.lot_formatted_note)
        # check if quantity is displayed in lot_formatted_note
        s_qty_lot = "(%s)" % formatLang(self.env, qty_lot)
        self.assertIn(s_qty_lot, line.lot_formatted_note)

    def test_01_sale_stock_delivery_partial_invoice_product_lot(self):
        # update quantities with their related lots
        self.qty_on_hand(self.product, self.stock_location, 3, self.lot1)
        self.qty_on_hand(self.product, self.stock_location, 3, self.lot2)
        # confirm quotation
        self.sale.action_confirm()
        picking = self.sale.picking_ids[:1]
        picking.action_confirm()
        picking.action_assign()
        self.assertEqual(len(picking.mapped('pack_operation_ids')), 1)
        self.assertEqual(len(picking.mapped(
            'pack_operation_ids.pack_lot_ids')), 2)
        operation_lot1 = picking.pack_operation_ids.pack_lot_ids[0]
        self.assertIn('Lot 1', operation_lot1.lot_id.name)
        self.assertEqual(operation_lot1.qty_todo, 3)
        operation_lot2 = picking.pack_operation_ids.pack_lot_ids[1]
        self.assertIn('Lot 2', operation_lot2.lot_id.name)
        self.assertEqual(operation_lot2.qty_todo, 1)
        # deliver partially only one lot
        qty_lot1 = 2.0
        operation_lot1.action_add_quantity(qty_lot1)
        picking.pack_operation_product_ids.write({'qty_done': 2.0})
        backorder_wiz_id = picking.do_new_transfer()['res_id']
        backorder_wiz = self.env['stock.backorder.confirmation'].browse(
            [backorder_wiz_id])
        backorder_wiz.process()
        # create invoice
        inv_id = self.sale.action_invoice_create()
        invoice = self.env['account.invoice'].browse(inv_id)
        self.assertEqual(len(invoice.invoice_line_ids), 1)
        line = invoice.invoice_line_ids
        # We must have only one lot
        self.assertEqual(len(line.prod_lot_ids.ids), 1)
        self.assertEqual(line.prod_lot_ids.id, self.lot1.id)
        self.assertIn('Lot 1', line.lot_formatted_note)
        # check if quantity is displayed in lot_formatted_note
        s_qty_lot1 = "(%s)" % formatLang(self.env, qty_lot1)
        self.assertIn(s_qty_lot1, line.lot_formatted_note)

    def test_02_sale_stock_delivery_partial_invoice_product_lot(self):
        # update quantities with their related lots
        self.qty_on_hand(self.product, self.stock_location, 3, self.lot1)
        self.qty_on_hand(self.product, self.stock_location, 3, self.lot2)
        # confirm quotation
        self.sale.action_confirm()
        picking = self.sale.picking_ids[:1]
        picking.action_confirm()
        picking.action_assign()
        self.assertEqual(len(picking.mapped('pack_operation_ids')), 1)
        self.assertEqual(len(picking.mapped(
            'pack_operation_ids.pack_lot_ids')), 2)
        operation_lot1 = picking.pack_operation_ids.pack_lot_ids[0]
        self.assertIn('Lot 1', operation_lot1.lot_id.name)
        self.assertEqual(operation_lot1.qty_todo, 3)
        operation_lot2 = picking.pack_operation_ids.pack_lot_ids[1]
        self.assertIn('Lot 2', operation_lot2.lot_id.name)
        self.assertEqual(operation_lot2.qty_todo, 1)
        # deliver partially both lots
        qty_lot1 = 2.0
        qty_lot2 = 1.0
        operation_lot1.action_add_quantity(qty_lot1)
        operation_lot2.action_add_quantity(qty_lot2)
        picking.pack_operation_product_ids.write({'qty_done': 3.0})
        backorder_wiz_id = picking.do_new_transfer()['res_id']
        backorder_wiz = self.env['stock.backorder.confirmation'].browse(
            [backorder_wiz_id])
        backorder_wiz.process()
        # create invoice
        inv_id = self.sale.action_invoice_create()
        invoice = self.env['account.invoice'].browse(inv_id)
        self.assertEqual(len(invoice.invoice_line_ids), 1)
        line = invoice.invoice_line_ids
        # We must have two lots
        self.assertEqual(len(line.prod_lot_ids.ids), 2)
        self.assertIn(self.lot1.id, line.prod_lot_ids.ids)
        self.assertIn(self.lot2.id, line.prod_lot_ids.ids)
        self.assertIn('Lot 1', line.lot_formatted_note)
        self.assertIn('Lot 2', line.lot_formatted_note)
        # check if both quantities are displayed in lot_formatted_note
        s_qty_lot1 = "(%s)" % formatLang(self.env, qty_lot1)
        self.assertIn(s_qty_lot1, line.lot_formatted_note)
        s_qty_lot2 = "(%s)" % formatLang(self.env, qty_lot2)
        self.assertIn(s_qty_lot2, line.lot_formatted_note)
