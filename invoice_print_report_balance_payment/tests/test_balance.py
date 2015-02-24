# -*- encoding: utf-8 -*-
###############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2014 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
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

from __future__ import unicode_literals

import datetime

from openerp import netsvc
from openerp.tests.common import TransactionCase

YEAR = datetime.date.today().year


class TestInvoiceBalance(TransactionCase):
    """ Test Invoice Balance Computation """

    def setUp(self):
        super(TestInvoiceBalance, self).setUp()
        self._setup_partner()
        self._setup_product()
        self.inv_obj = self.registry("account.invoice")

    def _setup_partner(self):
        partner_obj = self.registry("res.partner")
        self.partner_id = self.ref("base.res_partner_12")
        self.account_id = partner_obj.browse(
            self.cr, self.uid, self.partner_id,
        ).property_account_receivable.id

    def _setup_product(self):
        self.product_id = self.ref("product.product_product_1")

    def _create_invoice(self, amount, date):
        cr, uid = self.cr, self.uid
        invoice_obj = self.inv_obj
        invoice_line_obj = self.registry("account.invoice.line")

        line_vals = invoice_line_obj.default_get(
            cr, uid, invoice_line_obj._all_columns)
        line_vals.update(
            invoice_line_obj.product_id_change(
                cr, uid, [], self.product_id, uom_id=line_vals.get("uom_id"),
                qty=1, partner_id=self.partner_id,
            )["value"]
        )
        line_vals.update({
            "product_id": self.product_id,
            "account_id": self.ref("account.a_sale"),
            "price_unit": amount,
            "quantity": 1,
        })
        vals = invoice_obj.default_get(cr, uid, invoice_obj._all_columns)
        vals.update({
            "partner_id": self.partner_id,
            "account_id": self.account_id,
            "date_invoice": date,
        })
        vals.update(
            invoice_obj.onchange_partner_id(cr, uid, [], "out_invoice",
                                            self.partner_id, date)["value"]
        )
        vals["invoice_line"] = [(0, 0, line_vals)]
        inv = invoice_obj.create(cr, uid, vals)
        invoice_obj.button_reset_taxes(cr, uid, [inv])
        wf_service = netsvc.LocalService("workflow")
        wf_service.trg_validate(
            uid, 'account.invoice', inv, 'invoice_open', cr)
        return inv

    def _create_payment(self, amount, date):
        cr, uid = self.cr, self.uid
        voucher_obj = self.registry("account.voucher")
        vals = voucher_obj.default_get(
            cr, uid, voucher_obj._all_columns,
            context={
                "default_partner_id": self.partner_id,
                "default_type": "receipt",
                "default_amount": amount,
                "default_date": date,
            }
        )
        vals.update(
            voucher_obj.onchange_partner_id(
                cr, uid, [],
                self.partner_id, vals["journal_id"], amount,
                vals["currency_id"], "receipt", date,
            )["value"]
        )
        if vals["line_dr_ids"]:
            vals["line_dr_ids"] = [(0, 0, v) for v in vals["line_dr_ids"]]
        if vals["line_cr_ids"]:
            vals["line_cr_ids"] = [(0, 0, v) for v in vals["line_cr_ids"]]

        vals.update(
            voucher_obj.onchange_line_ids(
                cr, uid, [],
                [(5, False, False)] + vals["line_dr_ids"],
                [(5, False, False)] + vals["line_cr_ids"],
                vals['amount'], vals['currency_id'], vals['type'],
            )["value"]
        )

        voucher_id = voucher_obj.create(cr, uid, vals)
        voucher_obj.proforma_voucher(cr, uid, [voucher_id])

    def test_basic(self):
        cr, uid = self.cr, self.uid
        inv = self.inv_obj.browse(
            cr, uid,
            self._create_invoice(50, "{0}-01-07".format(YEAR))
        )

        self.assertEquals(inv.previous_invoice_id.id, False,
                          "No previous invoice expected")

        self.assertEquals(inv.previous_balance, 0,
                          "Previous balance should be 0 for first invoice")

        self.assertEquals(inv.to_pay, 50,
                          "To Pay should be 50")

        self.assertEquals(inv.payment_total, 0,
                          "No previous payments")

    def test_previous_paid(self):
        cr, uid = self.cr, self.uid
        first = self._create_invoice(50, "{0}-01-07".format(YEAR))
        self._create_payment(50, "{0}-01-10".format(YEAR))

        new = self.inv_obj.browse(
            cr, uid,
            self._create_invoice(50, "{0}-02-07".format(YEAR)),
        )

        self.assertEquals(new.previous_invoice_id.id, first,
                          "Previous should be first invoice")

        self.assertEquals(new.previous_balance, 50,
                          "Previous balance should be 50")

        self.assertEquals(new.to_pay, 50,
                          "To Pay should be 50")

        self.assertEquals(new.payment_total, 50,
                          "Previous payments should be 50")

    def test_partially_paid(self):
        cr, uid = self.cr, self.uid
        first = self._create_invoice(50, "{0}-01-07".format(YEAR))
        self._create_payment(20, "{0}-01-10".format(YEAR))

        new = self.inv_obj.browse(
            cr, uid,
            self._create_invoice(50, "{0}-02-07".format(YEAR)),
        )

        self.assertEquals(new.previous_invoice_id.id, first,
                          "Previous should be first invoice")

        self.assertEquals(new.previous_balance, 50,
                          "Previous balance should be 50")

        self.assertEquals(new.to_pay, 80,
                          "To Pay should be 80")

        self.assertEquals(new.payment_total, 20,
                          "Previous payments should be 50")

    def test_same_day(self):
        cr, uid = self.cr, self.uid
        self._create_invoice(50, "{0}-01-07".format(YEAR))
        self._create_payment(40, "{0}-01-10".format(YEAR))

        second = self._create_invoice(50, "{0}-02-07".format(YEAR))
        new = self.inv_obj.browse(
            cr, uid,
            self._create_invoice(15, "{0}-02-07".format(YEAR)),
        )

        self.assertEquals(new.previous_invoice_id.id, second,
                          "Previous should be second invoice")

        self.assertEquals(new.previous_balance, 75,
                          "Previous balance should be 75")

        self.assertEquals(new.to_pay, 75,
                          "To Pay should be 75")

        self.assertEquals(new.payment_total, 0,
                          "Previous payments should be 0")
