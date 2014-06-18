# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Yannick Vaucher
#    Copyright 2013 Camptocamp SA
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

from openerp import pooler
from openerp.osv import orm
from openerp.tools.translate import _
from openerp.addons.base_report_assembler import report_assembler


class InvoicePDFReportAssembler(report_assembler.PDFReportAssembler):
    """InvoicePDFReportAssembler allows to merge multiple
    invoice reports into one pdf"""

    def _get_report_ids(self, cr, uid, ids, context=None):
        pool = pooler.get_pool(cr.dbname)
        user_obj = pool.get('res.users')
        company = user_obj.browse(cr, uid, uid, context=context).company_id
        report_ids = [r.report_id.id for r in company.assemble_invoice_report_ids]
        if not report_ids:
            msg = _("No report defined in Configuration -> Accounting for model invoice.")
            raise orm.except_orm(_('Error'), msg)
        return report_ids

InvoicePDFReportAssembler('report.invoice_report_assemblage',
                          'account.invoice',
                          None)
