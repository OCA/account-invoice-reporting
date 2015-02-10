# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 Ursa Informative Systems (<www.ursainfosystems.com>).
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
###############################################################################

###############################################################################
#
# Description:  Create sql views consisting of unreconciled customer/supplier
#               deposits. Unapplied customer deposits are used in customer
#               aging view
#
###############################################################################


from osv import osv, fields
import tools


class customer_unapplied(osv.osv):

    _name = 'account.voucher.customer.unapplied'
    _auto = False

    _columns = {
        'partner_id': fields.many2one(
            'res.partner',
            u'Partner',
            readonly=True
        ),
        'partner_name': fields.text('Name', readonly=True),
        'salesman': fields.many2one('res.users', u'Sales Rep', readonly=True),
        'avg_days_overdue': fields.integer(u'Avg Days Overdue', readonly=True),
        'oldest_invoice_date': fields.date(u'Invoice Date', readonly=True),
        'total': fields.float(u'Total', readonly=True),
        'days_due_01to30': fields.float(u'01/30', readonly=True),
        'days_due_31to60': fields.float(u'31/60', readonly=True),
        'days_due_61to90': fields.float(u'61/90', readonly=True),
        'days_due_91to120': fields.float(u'91/120', readonly=True),
        'days_due_121togr': fields.float(u'+121', readonly=True),
        'max_days_overdue': fields.integer(u'Days Overdue', readonly=True),
        'current': fields.float(u'Total', readonly=True),
        'invoice_ref': fields.char('Reference', size=128),
        'invoice_id': fields.many2one(
            'account.invoice',
            'Invoice',
            readonly=True
        ),
        'currency_name': fields.text('Currency', readonly=True),
        'comment': fields.text('Notes', readonly=True),
    }

    _order = "partner_name"

    def init(self, cr):

        query = """
               SELECT cast(100000000000 + av.id as bigint) as id,rp.id as partner_id, rp.name as partner_name, days_due as avg_days_overdue,
                      av.date as oldest_invoice_date, rc.name as currency_name,
                      CASE WHEN (select count(name) from account_move_line where name=av.number) >= 1
                           THEN (select -1 * (sum(credit) - sum(debit)) from account_move_line where name =av.number)
                           ELSE 0 END as total,
                      CASE WHEN (days_due BETWEEN 01 AND  30) and (select count(name) from account_move_line where name=av.number) >= 1
                           THEN (select -1 * (sum(credit) - sum(debit)) from account_move_line where name =av.number)
                           ELSE 0 END  AS "days_due_01to30",
                      CASE WHEN (days_due BETWEEN 31 AND  60) and (select count(name) from account_move_line where name=av.number) >= 1
                           THEN (select -1 * (sum(credit) - sum(debit)) from account_move_line where name =av.number)
                           ELSE 0 END  AS "days_due_31to60",
                      CASE WHEN (days_due BETWEEN 61 AND  90) and (select count(name) from account_move_line where name=av.number) >= 1
                           THEN (select -1 * (sum(credit) - sum(debit)) from account_move_line where name =av.number)
                           ELSE 0 END  AS "days_due_61to90",
                      CASE WHEN (days_due BETWEEN 91 AND  120) and (select count(name) from account_move_line where name=av.number) >= 1
                           THEN (select -1 * (sum(credit) - sum(debit)) from account_move_line where name =av.number)
                           ELSE 0 END  AS "days_due_91to120",
                      CASE WHEN (days_due >= 121) and (select count(name) from account_move_line where name=av.number) >= 1
                           THEN (select -1 * (sum(credit) - sum(debit)) from account_move_line where name =av.number)
                           ELSE 0 END  AS "days_due_121togr",
                      CASE when days_due < 0
                           THEN 0
                           ELSE days_due END as "max_days_overdue",
                      CASE WHEN days_due <=0 and (select count(name) from account_move_line where name=av.number) >= 1
                           THEN (select -1 * (sum(credit) - sum(debit)) from account_move_line where name =av.number)
                           ELSE 0 END as "current",
                           av.number as invoice_ref, -999 as "invoice_id", null as comment, null as salesman
               FROM account_voucher av,res_partner rp, res_currency rc, account_move_line aml
               INNER JOIN
                  ( SELECT id, EXTRACT(DAY FROM (now() - (aml2.date + INTERVAL '30 days'))) AS days_due  FROM account_move_line aml2 ) DaysDue
                  ON DaysDue.id = aml.id
               LEFT JOIN account_invoice as ai
                  ON ai.move_id = aml.id
               WHERE av.partner_id = rp.id
                       and av.number = aml.name
                       and ai.currency_id = rc.id
                       and av.move_id in (select move_id from account_move_line where reconcile_id is null and
                       account_id in (select id from account_account where type = 'receivable'))
                       and av.state = 'posted'
                       and aml.credit > 0
        """
        tools.drop_view_if_exists(cr, '%s' % (self._name.replace('.', '_')))
        cr.execute("""
                      CREATE OR REPLACE VIEW %s AS ( %s)
        """ % (self._name.replace('.', '_'), query))
