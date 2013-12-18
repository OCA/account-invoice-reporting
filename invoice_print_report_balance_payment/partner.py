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

import datetime

from openerp.osv import orm


class res_partner(orm.Model):
    _inherit = 'res.partner'

    def get_balance_at_date(self, cr, uid, id, date, context=None):
        query = self.pool.get('account.move.line')._query_get(
            cr, uid, context=context)
        if isinstance(date, datetime.date):
            date = date.strftime('%Y-%m-%d')
        sql = """SELECT SUM(l.debit-l.credit)
                 FROM account_move_line l
                 JOIN account_move m ON (l.move_id=m.id)
                 LEFT JOIN account_account a ON (l.account_id=a.id)
                 WHERE a.type IN ('receivable','payable')
                 AND l.partner_id = %s
                 AND m.date <= '%s'
                 AND %s
        """ % (id, date, query)
        cr.execute(sql)
        row = cr.fetchone()
        return row[0] if row is not None else 0
