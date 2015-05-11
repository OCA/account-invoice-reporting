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


from openerp import fields, tools, models, api


class partner_aging_supplier(models.Model):

    _name = 'partner.aging.supplier'
    _auto = False

    @api.multi
    def invopen(self, context=None):
        """
        @description  Create link to view each listed invoice
        """
        models = self.pool.get('ir.model.data')
        view = models.get_object_reference('account', 'invoice_form')
        view_id = view and view[1] or False

        if not context:
            context = {}
        inv_id = self.invoice_id.id

        return {
            'name': ('Supplier Invoices'),
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': [view_id],
            'res_model': 'account.invoice',
            'context': "{'type':'out_invoice'}",
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            'res_id': inv_id,
        }

    partner_id = fields.Many2one('res.partner', u'Partner', readonly=True)
    partner_name = fields.Text('Name', readonly=True)
    max_days_overdue = fields.Integer(u'Days Overdue', readonly=True)
    avg_days_overdue = fields.Integer(u'Avg Days Overdue', readonly=True)
    oldest_invoice_date = fields.Date(u'Invoice Date', readonly=True)
    date_due = fields.Date(u'Due Date', readonly=True)
    total = fields.Float(u'Total', readonly=True)
    current = fields.Float(u'Current', readonly=True)
    days_due_01to30 = fields.Float(u'01/30', readonly=True)
    days_due_31to60 = fields.Float(u'31/60', readonly=True)
    days_due_61to90 = fields.Float(u'61/90', readonly=True)
    days_due_91to120 = fields.Float(u'91/120', readonly=True)
    days_due_121togr = fields.Float(u'+121', readonly=True)
    invoice_ref = fields.Char('Their Invoice', size=25, readonly=True)
    invoice_id = fields.Many2one('account.invoice', 'Invoice', readonly=True)
    comment = fields.Text('Notes', readonly=True)

    _order = 'date_due'

    def init(self, cr):
        """
        @description  Populate supplier aging view with up to date data on load
        """

        query = """
SELECT * from (
SELECT l.id as id,
       l.partner_id as partner_id,
       res_partner.name as "partner_name",
    CASE WHEN ai.id is not null
      THEN ai.date_due
    ElSE l.date_maturity
    END as "date_due",
    days_due as "avg_days_overdue",
    l.date as "oldest_invoice_date",
    CASE WHEN (l.credit - l.debit) > 0 and ai.id is not null THEN ai.residual
         WHEN (l.credit - l.debit) < 0 and ai.id is not null
           THEN -1*ai.residual
           ELSE l.credit - l.debit END as "total",
    CASE WHEN (l.credit - l.debit) > 0
           and (days_due BETWEEN 01 AND  30)
           and ai.id is not null
           then ai.residual
         WHEN (l.credit - l.debit) < 0
           and (days_due BETWEEN 01 AND  30)
           and ai.id is not null
           then -1*ai.residual
         WHEN (days_due BETWEEN 01 and 30)
           and ai.id is null
           THEN l.credit - l.debit
    ELSE 0
    END  AS "days_due_01to30",
    CASE WHEN (l.credit - l.debit) > 0
           and (days_due BETWEEN 31 AND  60)
           and ai.id is not null
           then ai.residual
         WHEN (l.credit - l.debit) < 0
           and (days_due BETWEEN 31 AND  60)
           and ai.id is not null
           then -1*ai.residual
         WHEN (days_due BETWEEN 31 and 60)
           and ai.id is null
           THEN l.credit - l.debit
    ELSE 0
    END  AS "days_due_31to60",
    CASE WHEN (l.credit - l.debit) > 0
           and (days_due BETWEEN 61 AND  90)
           and ai.id is not null
           then ai.residual
         WHEN (l.credit - l.debit) < 0
           and (days_due BETWEEN 61 AND  90)
           and ai.id is not null
           then -1*ai.residual
         WHEN (days_due BETWEEN 61 and 90)
           and ai.id is null
           THEN l.credit - l.debit
    ELSE 0
    END  AS "days_due_61to90",
    CASE WHEN (l.credit - l.debit) > 0
           and (days_due BETWEEN 91 AND 120)
           and ai.id is not null
           then ai.residual
         WHEN (l.credit - l.debit) < 0
           and (days_due BETWEEN 91 AND 120)
           and ai.id is not null
           then -1*ai.residual
         WHEN (days_due BETWEEN 91 and 120)
           and ai.id is null
           THEN l.credit - l.debit
    ELSE 0
    END  AS "days_due_91to120",
    CASE WHEN (l.credit - l.debit) > 0
           and days_due >= 121
           and ai.id is not null
           then ai.residual
         WHEN (l.credit - l.debit) < 0
           and days_due >= 121
           and ai.id is not null
           then -1*ai.residual
         WHEN days_due >= 121
           and ai.id is null
           THEN l.credit - l.debit
    ELSE 0
    END AS "days_due_121togr",
    CASE when (l.credit - l.debit) > 0
           and days_due <= 0
           and ai.id is not null
           then ai.residual
         WHEN (l.credit - l.debit) < 0
           and days_due <= 0
           and ai.id is not null
           then -1*ai.residual
         WHEN days_due <= 0
           and ai.id is null
           THEN l.credit - l.debit
    ELSE 0
    END as "current",
    CASE when days_due < 0 THEN 0 ELSE days_due END as "max_days_overdue",
    ai.supplier_invoice_number as "invoice_ref",
    ai.id as "invoice_id", ai.comment

    FROM account_move_line as l
INNER JOIN
  (
   SELECT lt.id,
   CASE WHEN inv.date_due is null then 0
   WHEN inv.id is not null THEN EXTRACT(DAY FROM (now() - inv.date_due))
   ELSE EXTRACT(DAY FROM (now() - lt.date_maturity)) END AS days_due
   FROM account_move_line lt
     LEFT JOIN account_invoice inv on lt.move_id = inv.move_id
) DaysDue
ON DaysDue.id = l.id

INNER JOIN account_account
   ON account_account.id = l.account_id
INNER JOIN res_company
   ON account_account.company_id = res_company.id
INNER JOIN account_move
   ON account_move.id = l.move_id
LEFT JOIN account_invoice as ai
   ON ai.move_id = l.move_id
INNER JOIN res_partner
   ON res_partner.id = l.partner_id
WHERE account_account.active
  AND (account_account.type IN ('payable'))
  AND (l.reconcile_id IS NULL)
  AND account_move.state = 'posted'
  AND days_due IS NOT NULL
) sq
"""

        tools.drop_view_if_exists(cr, '%s' % (self._name.replace('.', '_')))
        cr.execute("""
                      CREATE OR REPLACE VIEW %s AS ( %s)
        """ % (self._name.replace('.', '_'), query))
