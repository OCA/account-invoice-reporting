# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Agile Business Group <http://www.agilebg.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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

from openerp import models, fields


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    delivery_address_id = fields.Many2one(
        comodel_name='res.partner',
        string='Delivery Address',
        compute='_compute_delivery_address')
    sale_order_ids = fields.Many2many(
        'sale.order', 'sale_order_invoice_rel', 'invoice_id', 'order_id',
        'Sale orders', readonly=True, copy=False)

    def _compute_delivery_address(self):
        for record in self:
            delivery_address = False
            if record.picking_ids:
                if len(record.picking_ids) != 0:
                    partner_to_check = record.picking_ids[0].partner_id
                    for picking in record.picking_ids:
                        if partner_to_check != picking.partner_id:
                            delivery_address = False
                            break
                    delivery_address = partner_to_check
            if not delivery_address:
                if record.sale_order_ids:
                    if len(record.sale_order_ids) != 0:
                        partner_to_check = (
                            record.sale_order_ids[0].partner_shipping_id)
                        for so in record.sale_order_ids:
                            if partner_to_check != so.partner_shipping_id:
                                delivery_address = False
                                break
                        delivery_address = partner_to_check
            record.delivery_address_id = delivery_address
