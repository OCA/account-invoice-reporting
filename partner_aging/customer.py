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


from openerp.osv import fields, osv
import tools


class account_aging_customer(osv.osv):
    _name = 'partner.aging.customer'
    _auto = False

    def docopen(self, cr, uid, ids, context=None):
        """
        @description  Open document (invoice or payment) related to the
                      unapplied payment or outstanding balance on this line
        """
        if not context:
            context = {}
        models = self.pool.get('ir.model.data')
        # Get this line's invoice id
        inv_id = self.browse(cr, uid, ids[0]).invoice_id.id

        # if this is an unapplied payment(all unapplied payments hard-coded to
        # -999), get the referenced voucher
        if inv_id == -999:
            ref = self.browse(cr, uid, ids[0]).invoice_ref
            payment_pool = self.pool.get('account.voucher')
            # Get referenced customer payment (invoice_ref field is actually a
            # payment for these)
            voucher_id = payment_pool.search(
                cr,
                uid,
                [('number', '=', ref)]
            )[0]
            view = models.get_object_reference(
                cr,
                uid,
                'account_voucher',
                'view_voucher_form'
            )
            # Set values for form
            view_id = view and view[1] or False
            name = 'Customer Payments'
            res_model = 'account.voucher'
            ctx = "{}"
            doc_id = voucher_id
        # otherwise get the invoice
        else:
            view = models.get_object_reference(
                cr,
                uid,
                'account',
                'invoice_form'
            )
            view_id = view and view[1] or False
            name = 'Customer Invoices'
            res_model = 'account.invoice'
            ctx = "{'type':'out_invoice'}"
            doc_id = inv_id

        if not doc_id:
            return {}

        # Open up the document's form
        return {
            'name': (name),
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': [view_id],
            'res_model': res_model,
            'context': ctx,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            'res_id': doc_id,
        }

    _columns = {
        'partner_id': fields.many2one(
            'res.partner',
            u'Partner',
            readonly=True
        ),
        'partner_name': fields.text('Name', readonly=True),
        'avg_days_overdue': fields.integer(u'Avg Days Overdue', readonly=True),
        'date': fields.date(u'Due Date', readonly=True),
        'total': fields.float(u'Total', readonly=True),
        'days_due_01to30': fields.float(u'01/30', readonly=True),
        'days_due_31to60': fields.float(u'31/60', readonly=True),
        'days_due_61to90': fields.float(u'61/90', readonly=True),
        'days_due_91to120': fields.float(u'91/120', readonly=True),
        'days_due_121togr': fields.float(u'+121', readonly=True),
        'max_days_overdue': fields.integer(
            u'Days Overdue',
            group_operator="max",
            readonly=True
        ),
        'current': fields.float(u'Total', readonly=True),
        'invoice_ref': fields.char('Reference', size=25, readonly=True),
        'invoice_id': fields.many2one(
            'account.invoice',
            'Invoice',
            readonly=True
        ),
        'currency_name': fields.text('Currency', readonly=True),
        'comment': fields.text('Notes', readonly=True),
        'salesman': fields.many2one('res.users', u'Sales Rep', readonly=True),
    }

    _order = 'partner_name'

    def init(self, cr):
        """
        @author       Ursa Information Systems
        @description  Update table on load with latest aging information
        """
        query = """
SELECT id,
       partner_id,
       partner_name,
       salesman,
       avg_days_overdue,
       oldest_invoice_date AS date,
       total,
       days_due_01to30,
       days_due_31to60,
       days_due_61to90,
       days_due_91to120,
       days_due_121togr,
       max_days_overdue,
       current,
       invoice_ref,
       invoice_id,
       comment,
       currency_name
FROM   account_voucher_customer_unapplied
UNION
SELECT *
FROM   (SELECT l.id                AS id,
               l.partner_id        AS partner_id,
               res_partner.name    AS "partner_name",
               res_partner.user_id AS salesman,
               days_due            AS "avg_days_overdue",
               CASE
                 WHEN ai.id IS NOT NULL THEN ai.date_due
                 ELSE l.date_maturity
               end                 AS "date",
               CASE
                 WHEN ai.id IS NOT NULL THEN
                   CASE
                     WHEN ai.type = 'out_refund' THEN -1 * ai.residual
                     ELSE ai.residual
                   end
                 WHEN ai.id IS NULL THEN l.debit - l.credit
                 ELSE 0
               end                 AS "total",
               CASE
                 WHEN ( days_due BETWEEN 01 AND 30 )
                      AND ai.id IS NOT NULL THEN
                   CASE
                     WHEN ai.type = 'out_refund' THEN -1 * ai.residual
                     ELSE ai.residual
                   end
                 WHEN ( days_due BETWEEN 01 AND 30 )
                      AND ai.id IS NULL THEN l.debit - l.credit
                 ELSE 0
               end                 AS "days_due_01to30",
               CASE
                 WHEN ( days_due BETWEEN 31 AND 60 )
                      AND ai.id IS NOT NULL THEN
                   CASE
                     WHEN ai.type = 'out_refund' THEN -1 * ai.residual
                     ELSE ai.residual
                   end
                 WHEN ( days_due BETWEEN 31 AND 60 )
                      AND ai.id IS NULL THEN l.debit - l.credit
                 ELSE 0
               end                 AS "days_due_31to60",
               CASE
                 WHEN ( days_due BETWEEN 61 AND 90 )
                      AND ai.id IS NOT NULL THEN
                   CASE
                     WHEN ai.type = 'out_refund' THEN -1 * ai.residual
                     ELSE ai.residual
                   end
                 WHEN ( days_due BETWEEN 61 AND 90 )
                      AND ai.id IS NULL THEN l.debit - l.credit
                 ELSE 0
               end                 AS "days_due_61to90",
               CASE
                 WHEN ( days_due BETWEEN 91 AND 120 )
                      AND ai.id IS NOT NULL THEN
                   CASE
                     WHEN ai.type = 'out_refund' THEN -1 * ai.residual
                     ELSE ai.residual
                   end
                 WHEN ( days_due BETWEEN 91 AND 120 )
                      AND ai.id IS NULL THEN l.debit - l.credit
                 ELSE 0
               end                 AS "days_due_91to120",
               CASE
                 WHEN days_due >= 121
                      AND ai.id IS NOT NULL THEN
                   CASE
                     WHEN ai.type = 'out_refund' THEN -1 * ai.residual
                     ELSE ai.residual
                   end
                 WHEN days_due >= 121
                      AND ai.id IS NULL THEN l.debit - l.credit
                 ELSE 0
               end                 AS "days_due_121togr",
               CASE
                 WHEN days_due < 0 THEN 0
                 ELSE days_due
               end                 AS "max_days_overdue",
               CASE
                 WHEN days_due <= 0
                      AND ai.id IS NOT NULL THEN
                   CASE
                     WHEN ai.type = 'out_refund' THEN -1 * ai.residual
                     ELSE ai.residual
                   end
                 WHEN days_due <= 0
                      AND ai.id IS NULL THEN l.debit - l.credit
                 ELSE 0
               end                 AS "current",
               l.ref               AS "invoice_ref",
               ai.id               AS "invoice_id",
               ai.comment,
               res_currency.name   AS "currency_name"
        FROM   account_move_line AS l
               INNER JOIN (SELECT lt.id,
                                  CASE
                                    WHEN inv.id IS NOT NULL THEN
                                    Extract(day FROM ( Now() - inv.date_due ))
                                    ELSE Extract(day FROM (
                                                 Now() - lt.date_maturity ))
                                  end AS days_due
                           FROM   account_move_line lt
                                  LEFT JOIN account_invoice inv
                                         ON lt.move_id = inv.move_id) DaysDue
                       ON DaysDue.id = l.id
               INNER JOIN account_account
                       ON account_account.id = l.account_id
               INNER JOIN res_company
                       ON account_account.company_id = res_company.id
               INNER JOIN account_move
                       ON account_move.id = l.move_id
               LEFT JOIN account_invoice AS ai
                      ON ai.move_id = l.move_id
               INNER JOIN res_partner
                       ON res_partner.id = l.partner_id
               INNER JOIN res_currency
                       ON res_currency.id = ai.currency_id
        WHERE  account_account.active
               AND ai.state <> 'paid'
               AND ( account_account.type IN ( 'receivable' ) )
               AND ( l.reconcile_id IS NULL )
               AND account_move.state = 'posted'
               AND DaysDue.days_due IS NOT NULL) sq
        """

        tools.drop_view_if_exists(cr, '%s' % (self._name.replace('.', '_')))
        cr.execute(
            "CREATE OR REPLACE VIEW %s AS ( %s)" %
            (self._name.replace('.', '_'), query)
        )
