# -*- coding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2013 Camptocamp SA (http://www.camptocamp.com)
#   @author Nicolas Bessi
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
from openerp.osv import orm


class AccountInvoiceLine(orm.Model):

    _inherit = 'account.invoice.line'

    def product_id_change(self, cr, uid, ids, product, uom_id,
                          qty=0, name='', type='out_invoice', partner_id=False,
                          fposition_id=False, price_unit=False, currency_id=False,
                          context=None, company_id=None):
        """Overwrite of product on change in order to set the product invoice description
        in invoice line note. We also set name of product in invoice line name"""

        # Can you feel the pain?
        res = super(AccountInvoiceLine, self).product_id_change(cr, uid, ids, product, uom_id,
                                                                qty=qty, name=name, type=type,
                                                                partner_id=partner_id,
                                                                fposition_id=fposition_id,
                                                                price_unit=price_unit,
                                                                currency_id=currency_id,
                                                                context=context,
                                                                company_id=company_id)
        if not product:
            return res
        pobj = self.pool['product.product']
        product_name = pobj.name_get(cr, uid, [product], context=context)[0][1]
        product_note = pobj.read(cr, uid, product, ['description'], context=context)
        res['value']['name'] = product_name
        res['value']['formatted_note'] = product_note['description']
        return res
