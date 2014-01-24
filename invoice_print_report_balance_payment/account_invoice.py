# -*- encoding: utf-8 -*-
###############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from openerp.osv import orm, fields


class account_invoice(orm.Model):
    _inherit = 'account.invoice'

    def _previous_invoice_get(self, cr, uid, ids, field_names, arg, context=None):
        res = {}
        for invoice in self.browse(cr, uid, ids, context=context):
            domain = [
                ('date_invoice', '<', invoice.date_invoice),
                ('partner_id', '=', invoice.partner_id.id),
            ]
            search_result = self.search(
                cr, uid, domain, limit=1, order='date_invoice desc')
            res[invoice.id] = search_result[0] if search_result else False
        return res

    def _previous_balance_get(self, cr, uid, ids, field_names, arg, context=None):
        res = {}
        partner_obj = self.pool.get('res.partner')
        for invoice in self.browse(cr, uid, ids, context=context):
            if invoice.previous_invoice_id:
                res[invoice.id] = partner_obj.get_balance_at_date(
                    cr, uid, invoice.partner_id.id, invoice.previous_invoice_id.date_invoice,
                    context=context
                )
            else:
                res[invoice.id] = 0.0
        return res

    def _to_pay_get(self, cr, uid, ids, field_names, arg, context=None):
        res = {}
        partner_obj = self.pool.get('res.partner')
        for invoice in self.browse(cr, uid, ids, context=context):
            res[invoice.id] = partner_obj.get_balance_at_date(
                cr, uid, invoice.partner_id.id, invoice.date_invoice,
                context=context
            )
        return res

    def _payment_total_get(self, cr, uid, ids, field_names, arg, context=None):
        res = {}
        for invoice in self.browse(cr, uid, ids, context=context):
            res[invoice.id] = invoice.previous_balance - \
                (invoice.to_pay - invoice.amount_total)
        return res

    _columns = {
        'previous_invoice_id': fields.function(_previous_invoice_get, type='many2one', relation='account.invoice'),
        'previous_balance': fields.function(_previous_balance_get, type='float'),
        'to_pay': fields.function(_to_pay_get, type='float'),
        'payment_total': fields.function(_payment_total_get, type='float'),
    }

    def invoice_print(self, cr, uid, ids, context=None):
        result = super(account_invoice, self).invoice_print(
            cr, uid, ids, context=context)
        result['report_name'] = 'account.invoice.balance_payment'
        return result
