# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Eficent (<http://www.eficent.com/>)
#              Jordi Ballester Alomar <jordi.ballester@eficent.com>
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
##############################################################################
from openerp.osv import fields, orm


class AccountInvoiceReport(orm.Model):
    _inherit = "account.invoice.report"

    _columns = {
        'internal_number': fields.char('Invoice Number', size=32,
                                       readonly=True,
                                       help="Unique number of the invoice, "
                                            "computed automatically when the "
                                            "invoice is created."),
        'supplier_invoice_number': fields.char(
            'Supplier Invoice Number', size=64,
            help="The reference of this invoice as provided by the supplier.",
            readonly=True),
        'number': fields.char('Journal Entry', readonly=True, size=64),
    }

    def _select(self):
        select_str = super(AccountInvoiceReport, self)._select()
        select_str += """, sub.internal_number, sub.supplier_invoice_number,
        sub.number"""
        return select_str

    def _sub_select(self):
        select_str = super(AccountInvoiceReport, self)._sub_select()
        select_str += """, ai.internal_number,
        ai.supplier_invoice_number, ai.number"""
        return select_str

    def _group_by(self):
        group_by_str = super(AccountInvoiceReport, self)._group_by()
        group_by_str += """, ai.internal_number, ai.supplier_invoice_number,
        ai.number"""
        return group_by_str
