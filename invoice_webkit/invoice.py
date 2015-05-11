# -*- coding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2011 Camptocamp SA (http://www.camptocamp.com)
#   @author Bessi Nicolas, Vincent Renaville
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
##############################################################################
from openerp.osv.orm import Model, fields
from openerp.osv import osv
from openerp.tools.translate import _


class InvoiceConditionText(Model):
    """add info condition in the invoice"""
    _name = "account.condition_text"
    _description = "Invoices conditions"

    _columns = {
        'name': fields.char('Condition summary', required=True, size=128),
        'type': fields.selection([('header', 'Top condition'),
                                  ('footer', 'Bottom condition')],
                                 'type', required=True),

        'text': fields.html('Condition', translate=True, required=True)}


class AccountInvoice(Model):
    """ Add account.condition_text to invoice"""

    _inherit = "account.invoice"

    def _set_condition(self, cr, uid, inv_id, commentid, key, partner_id=False):
        """Set the text of the notes in invoices"""
        if not commentid:
            return {}
        if not partner_id:
            raise osv.except_osv(_('No Customer Defined !'), _('Before choosing condition text select a customer.'))
        lang = self.pool.get('res.partner').browse(cr, uid, partner_id).lang or 'en_US'
        cond = self.pool.get('account.condition_text').browse(cr, uid, commentid, {'lang': lang})
        return {'value': {key: cond.text}}

    def set_header(self, cursor, uid, inv_id, commentid, partner_id=False):
        return self._set_condition(cursor, uid, inv_id, commentid, 'note1', partner_id)

    def set_footer(self, cursor, uid, inv_id, commentid, partner_id=False):
        return self._set_condition(cursor, uid, inv_id, commentid, 'note2', partner_id)

    _columns = {'text_condition1': fields.many2one('account.condition_text', 'Header condition',
                                                   domain=[('type', '=', 'header')]),
                'text_condition2': fields.many2one('account.condition_text', 'Footer condition',
                                                   domain=[('type', '=', 'footer')]),
                'note1': fields.html('Header'),
                'note2': fields.html('Footer'),
                }


class AccountInvoiceLine(Model):

    _inherit = 'account.invoice.line'

    _columns = {'formatted_note': fields.html('Formatted Note')}
