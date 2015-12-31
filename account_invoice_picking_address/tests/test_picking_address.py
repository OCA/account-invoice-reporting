# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Lorenzo Battistini - Agile Business Group
#    About license, see __openerp__.py file
#
##############################################################################

import openerp.tests.common as common


class TestAccountInvoiceParner(common.TransactionCase):

    def setUp(self):
        super(TestAccountInvoiceParner, self).setUp()
        self.so_model = self.env['sale.order']
        self.so_line_model = self.env['sale.order.line']
        self.global_solutions = self.env.ref('base.res_partner_21')
        self.kevin_clarke = self.env.ref('base.res_partner_address_34')
        self.headphones = self.env.ref('product.product_product_7')

    def test_0(self):
        so = self.so_model.create({
            'partner_id': self.global_solutions.id,
            'partner_shipping_id': self.kevin_clarke.id,
            })
        self.so_line_model.create({
            'order_id': so.id,
            'name': 'Apple In-Ear Headphones',
            'product_id': self.headphones.id,
            'price_unit': 100,
            })
        so.action_button_confirm()
        so.action_invoice_create()
        self.assertEqual(len(so.invoice_ids), 1)
        self.assertEqual(
            so.invoice_ids[0].delivery_address_id.id, self.kevin_clarke.id)
