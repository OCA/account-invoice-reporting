# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Agile Business Group sagl (<http://www.agilebg.com>)
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

from openerp import models, fields, api


class account_invoice(models.Model):
    _inherit = "account.invoice"

    delivery_address_id = fields.Many2one(
        comodel_name='res.partner',
        string='Delivery Address',
        compute='_compute_delivery_address',
        store=True)

    @api.depends('picking_ids')
    def _compute_delivery_address(self):
        for record in self:
            if record.picking_ids:
                if len(record.picking_ids) == 0:
                    record.delivery_address_id = False
                else:
                    partner_to_check = record.picking_ids[0].partner_id
                    for picking in record.picking_ids:
                        if partner_to_check != picking.partner_id:
                            record.delivery_address_id = False
                            break
                    record.delivery_address_id = partner_to_check
            else:
                record.delivery_address_id = False
