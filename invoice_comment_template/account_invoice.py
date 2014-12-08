# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Nicolas Bessi
#            Guewen Baconnier
#    Copyright 2013-2014 Camptocamp SA
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
from openerp import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    condition_template1_id = fields.Many2one('base.condition.template',
                                             string='Top Comment Template')
    condition_template2_id = fields.Many2one('base.condition.template',
                                             string='Bottom Comment Template')
    note1 = fields.Html('Top Comment')
    note2 = fields.Html('Bottom Comment')

    @api.onchange('condition_template1_id')
    def _set_note1(self):
        condition = self.condition_template1_id
        if condition:
            self.note1 = condition.get_value(self.partner_id.id)

    @api.onchange('condition_template2_id')
    def _set_note2(self):
        condition = self.condition_template2_id
        if condition:
            self.note2 = condition.get_value(self.partner_id.id)
