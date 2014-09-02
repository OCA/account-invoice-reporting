# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module Copyright (C) 2014 Therp BV (<http://therp.nl>).
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
'''Extend model account.invoice'''
from openerp.osv import orm, fields


class AccountInvoice(orm.Model):
    '''Modify account invoice to add delivery address'''
    _inherit = 'account.invoice'

    def _modify_vals(self, cr, uid, vals, browse_obj=None, context=None):
        '''Utility function called on create and write to deliver consistent
        values. In this case fill delivery address when possible.'''
        if 'partner_shipping_id' in vals:
            return  # do not overwrite when explicitly filled
        partner_id = False
        if browse_obj:
            # Do nothing when invoice no longer in draft or sent state
            # or when shipping id already set:
            if (not browse_obj.state in ['draft', 'sent']
                    or browse_obj.partner_shipping_id):
                return
            partner_id = (
                browse_obj.partner_id and browse_obj.partner_id.id or False)
        else:
            partner_id = vals.get('partner_id') or False
        if not partner_id:
            return
        # We have a partner, find delivery address
        partner_model = self.pool.get('res.partner')
        addr = partner_model.address_get(
            cr, uid, [partner_id], ['delivery'])
        vals['partner_shipping_id'] = addr['delivery']

    def create(self, cr, uid, vals, context=None):
        '''get delivery address, when not already in vals'''
        self._modify_vals(cr, uid, vals, browse_obj=None, context=context)
        return super(AccountInvoice, self).create(
            cr, uid, vals, context)

    def write(self, cr, uid, ids, vals, context=None):
        '''get delivery address, when not already in vals, or filled'''
        for item_id in ids:
            browse_records = self.browse(cr, uid, [item_id], context=context)
            browse_obj = browse_records[0]
            self._modify_vals(
                cr, uid, vals, browse_obj=browse_obj, context=context)
            super(AccountInvoice, self).write(
                cr, uid, [item_id], vals, context=context)
        return True

    _columns = {
        'partner_shipping_id': fields.many2one(
            'res.partner', 'Delivery Address',
            readonly=True,
            states={
                'draft': [('readonly', False)],
                'sent':  [('readonly', False)]
            },
            help="Delivery address for current invoice."),
    }
