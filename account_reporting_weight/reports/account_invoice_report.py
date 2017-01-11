# -*- coding: utf-8 -*-
# Copyright 2017 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models
import openerp.addons.decimal_precision as dp


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    weight = fields.Float(digits=dp.get_precision('Stock Weight'))

    def _select(self):
        select_str = super(AccountInvoiceReport, self)._select()
        select_str += """
            , sub.weight as weight
            """
        return select_str

    def _sub_select(self):
        select_str = super(AccountInvoiceReport, self)._sub_select()
        select_str += """
            , CASE
              WHEN u.category_id = imd.res_id
              THEN (
                CASE
                  WHEN ai.type::text = ANY (
                    ARRAY['out_refund'::character varying::text,
                          'in_invoice'::character varying::text])
                  THEN
                    SUM(-ail.quantity / u.factor * u2.factor)
                  ELSE
                    SUM(ail.quantity / u.factor * u2.factor)
                  END
                )
                ELSE (
                  CASE
                    WHEN ai.type::text = ANY (
                      ARRAY['out_refund'::character varying::text,
                            'in_invoice'::character varying::text])
                      THEN
                        SUM(pr.weight * -ail.quantity / u.factor * u2.factor)
                      ELSE
                        SUM(pr.weight * ail.quantity / u.factor * u2.factor)
                      END
                )
            END AS weight
            """
        return select_str

    def _from(self):
        from_str = super(AccountInvoiceReport, self)._from()
        from_str += """
            JOIN ir_model_data imd
                ON (imd.module = 'product' AND
                    imd.name = 'product_uom_categ_kgm')
            """
        return from_str

    def _group_by(self):
        group_by_str = super(AccountInvoiceReport, self)._group_by()
        group_by_str += ", pr.weight, u.category_id, imd.res_id"
        return group_by_str
