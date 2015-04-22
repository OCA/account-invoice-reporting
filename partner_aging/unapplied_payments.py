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
SELECT cast(100000000000 + av.id AS BIGINT) AS id
 ,rp.id AS partner_id
 ,rp.NAME AS partner_name
 ,days_due AS avg_days_overdue
 ,av.DATE AS oldest_invoice_date
 ,rc.NAME AS currency_name
 ,CASE
  WHEN (
    SELECT count(NAME)
    FROM account_move_line
    WHERE NAME = av.number
    ) >= 1
   THEN (
     SELECT - 1 * (sum(credit) - sum(debit))
     FROM account_move_line
     WHERE NAME = av.number
     )
  ELSE 0
  END AS total
 ,CASE
  WHEN (
    days_due BETWEEN 01
     AND 30
    )
   AND (
    SELECT count(NAME)
    FROM account_move_line
    WHERE NAME = av.number
    ) >= 1
   THEN (
     SELECT - 1 * (sum(credit) - sum(debit))
     FROM account_move_line
     WHERE NAME = av.number
     )
  ELSE 0
  END AS "days_due_01to30"
 ,CASE
  WHEN (
    days_due BETWEEN 31
     AND 60
    )
   AND (
    SELECT count(NAME)
    FROM account_move_line
    WHERE NAME = av.number
    ) >= 1
   THEN (
     SELECT - 1 * (sum(credit) - sum(debit))
     FROM account_move_line
     WHERE NAME = av.number
     )
  ELSE 0
  END AS "days_due_31to60"
 ,CASE
  WHEN (
    days_due BETWEEN 61
     AND 90
    )
   AND (
    SELECT count(NAME)
    FROM account_move_line
    WHERE NAME = av.number
    ) >= 1
   THEN (
     SELECT - 1 * (sum(credit) - sum(debit))
     FROM account_move_line
     WHERE NAME = av.number
     )
  ELSE 0
  END AS "days_due_61to90"
 ,CASE
  WHEN (
    days_due BETWEEN 91
     AND 120
    )
   AND (
    SELECT count(NAME)
    FROM account_move_line
    WHERE NAME = av.number
    ) >= 1
   THEN (
     SELECT - 1 * (sum(credit) - sum(debit))
     FROM account_move_line
     WHERE NAME = av.number
     )
  ELSE 0
  END AS "days_due_91to120"
 ,CASE
  WHEN (days_due >= 121)
   AND (
    SELECT count(NAME)
    FROM account_move_line
    WHERE NAME = av.number
    ) >= 1
   THEN (
     SELECT - 1 * (sum(credit) - sum(debit))
     FROM account_move_line
     WHERE NAME = av.number
     )
  ELSE 0
  END AS "days_due_121togr"
 ,CASE
  WHEN days_due < 0
   THEN 0
  ELSE days_due
  END AS "max_days_overdue"
 ,CASE
  WHEN days_due <= 0
   AND (
    SELECT count(NAME)
    FROM account_move_line
    WHERE NAME = av.number
    ) >= 1
   THEN (
     SELECT - 1 * (sum(credit) - sum(debit))
     FROM account_move_line
     WHERE NAME = av.number
     )
  ELSE 0
  END AS "current"
 ,av.number AS invoice_ref
 ,- 999 AS "invoice_id"
 ,NULL AS comment
 ,NULL AS salesman

FROM account_voucher av
 ,res_partner rp
 ,res_currency rc
 ,account_move_line aml

INNER JOIN (
 SELECT id
  ,EXTRACT(DAY FROM (now() - (aml2.DATE + INTERVAL '30 days'))) AS days_due
 FROM account_move_line aml2
 ) DaysDue ON DaysDue.id = aml.id

LEFT JOIN account_invoice AS ai ON ai.move_id = aml.id

WHERE av.partner_id = rp.id
 AND av.number = aml.NAME
 AND ai.currency_id = rc.id
 AND av.move_id IN (
  SELECT move_id
  FROM account_move_line
  WHERE reconcile_id IS NULL
   AND account_id IN (
    SELECT id
    FROM account_account
    WHERE type = 'receivable'
    )
  )
 AND av.STATE = 'posted'
 AND aml.credit > 0
        """

        tools.drop_view_if_exists(cr, '%s' % (self._name.replace('.', '_')))
        cr.execute(
            "CREATE OR REPLACE VIEW %s AS ( %s)" %
            (self._name.replace('.', '_'), query)
        )
