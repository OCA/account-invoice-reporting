# -*- coding: utf-8 -*-
# Copyright 2011 Domsense s.r.l. <http://www.domsense.com>
# Copyright 2013 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
# Copyright 2017 Vicent Cubells <vicent.cubells@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


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
        })
        cls.sale = cls.env['sale.order'].create({
            'partner_id': cls.partner.id,
            'partner_invoice_id': cls.partner.id,
            'partner_shipping_id': cls.partner.id,
            'order_line': [(0, 0, {
                'name': cls.product.name,
                'product_id': cls.product.id,
                'product_uom_qty': 2,
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

    def test_invoice_product_lot(self):
        # confirm quotation
        self.sale.action_confirm()
        picking = self.sale.picking_ids[:1]
        # set lots and transfer
        picking.action_confirm()
        picking.action_assign()
        picking.do_prepare_partial()
        self.env['stock.pack.operation'].create({
            'product_id': self.product.id,
            'product_qty': 1,
            'product_uom_id': self.product.uom_id.id,
            'location_id': self.stock_location.id,
            'location_dest_id': self.customer_location.id,
            'picking_id': picking.id,
            'pack_lot_ids': [(0, 0, {'lot_id': self.lot1.id, 'qty': 1.0})],
        })
        self.env['stock.pack.operation'].create({
            'product_id': self.product.id,
            'product_qty': 1,
            'product_uom_id': self.product.uom_id.id,
            'location_id': self.stock_location.id,
            'location_dest_id': self.customer_location.id,
            'picking_id': picking.id,
            'pack_lot_ids': [(0, 0, {'lot_id': self.lot2.id, 'qty': 1.0})],
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
