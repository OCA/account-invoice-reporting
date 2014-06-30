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


class InvoiceConditionText(Model):
    """add info condition in the invoice"""
    _name = "account.condition_text"
    _description = "Invoices conditions"

    _columns = {
        'name': fields.char('Condition summary', required=True, size=128),
        'type': fields.selection([('header','Top condition'),
                                   ('footer', 'Bottom condition')],
                                    'type', required=True),

        'text': fields.html('Condition', translate=True, required=True)}

class AccountInvoice(Model):
    """ Add account.condition_text to invoice"""

    _inherit = "account.invoice"

    def _set_condition(self, cr, uid, inv_id, commentid, key):
        """Set the text of the notes in invoices"""
        if not commentid:
            return {}
        try :
            lang = self.browse(cr, uid, inv_id)[0].partner_id.lang
        except :
            lang = 'en_US'
        cond = self.pool.get('account.condition_text').browse(cr, uid, commentid, {'lang': lang})
        return {'value': {key: cond.text}}

    def set_header(self, cr, uid, inv_id, commentid):
        return self._set_condition(cr, uid, inv_id, commentid, 'note1')

    def set_footer(self, cr, uid, inv_id, commentid):
        return self._set_condition(cr, uid, inv_id, commentid, 'note2')

    _columns = {'text_condition1': fields.many2one('account.condition_text', 'Header condition',
                                                   domain=[('type', '=', 'header')]),
                'text_condition2': fields.many2one('account.condition_text', 'Footer condition',
                                                   domain=[('type', '=', 'footer')]),
                'note1': fields.html('Header'),
                'note2': fields.html('Footer'),}


class AccountInvoiceLine(Model):

    _inherit = 'account.invoice.line'

    _columns = {'formatted_note': fields.html('Formatted Note')}
