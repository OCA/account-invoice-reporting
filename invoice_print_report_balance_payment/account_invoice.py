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

from datetime import datetime, timedelta

from openerp.osv import orm, fields
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT


def to_date(datestr):
    return datetime.strptime(datestr, DEFAULT_SERVER_DATE_FORMAT)


def invoice_amount(invoice):
    if invoice.type in ('out_invoice', 'in_refund'):
        return invoice.amount_total
    else:
        return -1 * invoice.amount_total


class AccountInvoice(orm.Model):
    _inherit = 'account.invoice'

    def _get_day_payments(self, cr, uid, partner_id, date):
        pay_obj = self.pool["account.voucher"]
        payments = pay_obj.read_group(
            cr, uid, [
                ('partner_id', '=', partner_id),
                ('state', '=', 'posted'),
                ('date', '=', date),
                ('type', '=', 'receipt'),
            ],
            fields=["amount", "type"],
            groupby="type",
        )
        return payments[0]["amount"] if payments else 0

    def _get_balance_payment(self, cr, uid, ids, field_names, arg,
                             context=None):
        res = {}
        partner_obj = self.pool["res.partner"]
        date_balances = {}

        def day_balance(partner_id, date):
            key = (partner_id, date)
            if key in date_balances:
                return date_balances[key]
            balance = partner_obj.get_balance_at_date(
                cr, uid, partner_id, date,
                context=context
            ) or 0
            date_balances[key] = balance
            return balance

        for invoice in self.browse(cr, uid, sorted(ids, reverse=True),
                                   context=context):
            if invoice.id in res:
                continue

            domain = [('partner_id', '=', invoice.partner_id.id)]
            prev_day = domain + [('date_invoice', '<', invoice.date_invoice)]
            same_day = domain + [('date_invoice', '=', invoice.date_invoice)]
            last_previous = self.search(cr, uid, prev_day, limit=1,
                                        order='date_invoice desc, id desc')
            balance = prev_balance = 0
            if last_previous:
                last = self.browse(cr, uid, last_previous[0], context=context)
                prev_balance = day_balance(last.partner_id.id,
                                           last.date_invoice)
            else:
                last = False

            same_day = self.search(cr, uid, same_day, order='id')
            # First handle the first invoice of the day
            first = self.browse(cr, uid, same_day[0], context=context)
            if not first:
                first = invoice

            # Get day before balance:
            prev_day_balance = day_balance(
                invoice.partner_id.id,
                to_date(invoice.date_invoice) - timedelta(days=1),
            )
            day_payments = self._get_day_payments(cr, uid,
                                                  first.partner_id.id,
                                                  first.date_invoice)
            first_balance = sum([
                prev_day_balance,
                -1 * day_payments,
                invoice_amount(first),
            ])
            res[first.id] = {
                "previous_invoice_id": last.id if last else False,
                "previous_balance": prev_balance,
                "to_pay": first_balance,
                "payment_total": sum([
                    (prev_balance - prev_day_balance),
                    day_payments,
                ]),
            }

            # Now process other invoices on the same day
            if len(same_day) <= 1:
                continue

            previous = first.id
            prev_balance = first_balance
            for day_invoice in self.browse(cr, uid, same_day[1:],
                                           context=context):
                balance = prev_balance + invoice_amount(day_invoice)
                res[day_invoice.id] = {
                    "previous_invoice_id": previous,
                    "previous_balance": prev_balance,
                    "to_pay": balance,
                    "payment_total": 0,
                }
                previous = day_invoice.id
                prev_balance = balance

        return res

    _columns = {
        'previous_invoice_id': fields.function(
            _get_balance_payment, type='many2one',
            multi="balance_payment",
            relation='account.invoice'),
        'previous_balance': fields.function(
            _get_balance_payment, type='float',
            multi="balance_payment"),
        'to_pay': fields.function(
            _get_balance_payment, type='float',
            multi="balance_payment"),
        'payment_total': fields.function(
            _get_balance_payment, type='float',
            multi="balance_payment"),
    }

    def invoice_print(self, cr, uid, ids, context=None):
        result = super(AccountInvoice, self).invoice_print(
            cr, uid, ids, context=context)
        result['report_name'] = 'account.invoice.balance_payment'
        return result
