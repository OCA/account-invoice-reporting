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
from datetime import date


class TestProdLot(common.TransactionCase):

    def setUp(self):
        super(TestProdLot, self).setUp()
        self.sale_order = self.env["sale.order"]
        self.stock_move = self.env["stock.move"]
        self.stock_picking = self.env["stock.picking"]
        self.account_invoice = self.env["account.invoice"]
        self.stock_transfer_details = self.registry("stock.transfer_details")
        self.stock_invoice = self.registry("stock.invoice.onshipping")
        self.model_data = self.env['ir.model.data']


    def getDemoObject(self, module, data_id):
        if module == '':
            module = 'account_invoice_production_lot'
        xmlid = '%s.%s' % (module, data_id)
        return self.model_data.xmlid_to_object(xmlid)

    def getIdDemoObj(self, module, data_id):
        return self.getDemoObject(module, data_id).id

    def run_picking(self, pick, lot_ids, split=False):
        cr = self.env.cr
        uid = self.env.uid
        context = self.env.context.copy()
        context.update(
            {
                'active_model': 'stock.picking',
                'active_ids': [pick.id],
                # 'active_id': len([pick.id]) and pick.id or False
            }
        )
        pick_wizard_id = self.stock_transfer_details.create(
            cr, uid, {}, context)
        pick_wizard = self.stock_transfer_details.browse(
            cr, uid, pick_wizard_id)
        if split:
            pick_wizard.item_ids[0].split_quantities()
        pick_wizard.item_ids[0].write({'lot_id': lot_ids[0].id})
        return self.stock_transfer_details.do_detailed_transfer(
            cr, uid, [pick_wizard_id], context)

    def run_create_invoice(self, pick):
        cr = self.env.cr
        uid = self.env.uid
        context = self.env.context.copy()
        context.update({'active_ids': [pick.id]})
        inv_wizard_id = self.stock_invoice.create(
            cr, uid,
            {
                'invoice_date': date.today().strftime('%Y-%m-%d')
            }, context)
        return self.stock_invoice.create_invoice(
            cr, uid, [inv_wizard_id], context)

    def test_0_SaleOrder(self):
        """
        Test Sale Order 1
       """
        lot_ids = []
        lot_ids.append(self.getDemoObject('', 'lot_icecream_0'))
        order = self.getDemoObject('', 'sale_order_0')
        order.signal_workflow('order_confirm')
        for pick in order.picking_ids:
            data = pick.force_assign()
            self.assertEqual(pick.state, 'assigned')
            if data:
                trans = self.run_picking(pick, lot_ids)
                if trans and pick.action_done():
                    self.assertEqual(pick.state, 'done')
                    invoice_id = self.run_create_invoice(pick)
                    invoice = self.account_invoice.browse(invoice_id)
                    invoice.load_lines_lots()
                    self.assertEqual(
                        invoice.invoice_line[0].prod_lot_ids[0].name,
                        'Lot0 for Ice cream'
                    )
