# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2015 Agile Business Group <http://www.agilebg.com>
#    Copyright (C) 2015 Alessio Gerace <alesiso.gerace@agilebg.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.tests import common


class TestProdLot(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestProdLot, cls).setUpClass()

        cls.product = cls.env['product.product'].create({
            'name': 'Product Test',
            'type': 'product'
        })

        cls.lot1 = cls.env['stock.production.lot'].create({
            'name': 'Lot 1',
            'product_id': cls.product.id
        })

        cls.lot2 = cls.env['stock.production.lot'].create({
            'name': 'Lot 2',
            'product_id': cls.product.id
        })

        cls.partner = cls.env['res.partner'].create({
            'name': 'Test partner'
        })

        cls.sale = cls.env['sale.order'].create({
            'partner_id': cls.partner.id,
            'partner_invoice_id': cls.partner.id,
            'partner_shipping_id': cls.partner.id,
            'order_line': [
                (0, 0, {
                    'product_id': cls.product.id,
                    'name': cls.product.name,
                    'product_uom_qty': 2,
                    'product_uom': cls.product.uom_id.id,
                    'price_unit': 15.0
                })
            ]
        })

        cls.stock_location = cls.env.ref('stock.stock_location_stock')
        cls.customer_location = cls.env.ref('stock.stock_location_customers')
        cls.picking_type_out = cls.env.ref('stock.picking_type_out')

    def test_invoice_line_lots(self):
        self.sale.action_confirm()
        picking = self.sale.picking_ids[:1]

        picking.action_confirm()
        picking.action_assign()

        picking.do_prepare_partial()

        self.env['stock.pack.operation'].create({
            'product_id': self.product.id,
            'product_qty': 2,
            'product_uom_id': self.product.uom_id.id,
            'location_id': self.stock_location.id,
            'location_dest_id': self.customer_location.id,
            'picking_id': picking.id,
            'pack_lot_ids': [
                (0, 0, {'lot_id': self.lot1.id, 'qty': 1}),
                (0, 0, {'lot_id': self.lot2.id, 'qty': 1})
            ]
        })

        picking.do_transfer()

        invoice_id = self.sale.action_invoice_create()
        invoice = self.env['account.invoice'].browse(invoice_id)

        self.assertEqual(len(invoice.invoice_line_ids), 1)
        self.assertEqual(len(invoice.invoice_line_ids.prod_lot_ids.ids), 2)
        self.assertIn('Lot 1', invoice.invoice_line_ids.lot_formatted_note)
        self.assertIn('Lot 2', invoice.invoice_line_ids.lot_formatted_note)
