# -*- coding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2011 Camptocamp SA (http://www.camptocamp.com)
#   @author Bessi Nicolas, Vicent Renaville
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
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

        'text': fields.text('Condition', translate=True, required=True)}

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

    _columns = {'text_condition1': fields.many2one('account.condition_text', 'Header condition'),
                'text_condition2': fields.many2one('account.condition_text', 'Footer condition'),
                'note1': fields.text('Header'),
                'note2': fields.text('Footer'),}


class AccountInvoiceLine(Model):

    _inherit = 'account.invoice.line'

    _columns = {'formatted_note': fields.html('Note formatée')}
