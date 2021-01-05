# Copyright 2018 Tecnativa - Vicent Cubells
# Copyright 2020 Tecnativa - Víctor Martínez
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from datetime import timedelta

import babel

from odoo import fields
from odoo.tests import common
from odoo.tests.common import Form
from odoo.tools import posix_to_ldml, pycompat


class TestInvoiceReportDueList(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.account_tax = cls.env["account.tax"].create(
            {"name": "0%", "amount_type": "fixed", "type_tax_use": "sale", "amount": 0}
        )
        cls.payment_term_normal = cls.env["account.payment.term"].create(
            {
                "name": "One Time Payment Term",
                "line_ids": [(0, 0, {"value": "balance", "days": 30})],
            }
        )
        cls.payment_term_multi = cls.env["account.payment.term"].create(
            {
                "name": "Twice Payment Term",
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "value": "percent",
                            "value_amount": 25.0,
                            "days": 30,
                            "sequence": 10,
                        },
                    ),
                    (0, 0, {"value": "balance", "days": 60, "sequence": 20}),
                ],
            }
        )
        cls.partner = cls.env["res.partner"].create({"name": "Partner test"})
        cls.product_id = cls.env["product.product"].create(
            {"name": "Product Test", "taxes_id": [(6, 0, [cls.account_tax.id])]}
        )
        cls.account = cls.env["account.account"].create(
            {
                "name": "Test Account",
                "code": "TEST",
                "user_type_id": cls.env.ref("account.data_account_type_receivable").id,
                "reconcile": True,
            }
        )
        cls.other_account = cls.env["account.account"].create(
            {
                "name": "Test Account",
                "code": "ACC",
                "user_type_id": cls.env.ref(
                    "account.data_account_type_other_income"
                ).id,
                "reconcile": True,
            }
        )

    def test_due_list(self, move_type="out_invoice"):
        move_form = Form(self.env["account.move"].with_context(default_type=move_type))
        move_form.partner_id = self.partner
        move_form.invoice_payment_term_id = self.payment_term_normal
        with move_form.invoice_line_ids.new() as line_form:
            line_form.product_id = self.product_id
            line_form.price_unit = 100.0
        invoice = move_form.save()
        self.assertFalse(invoice.multi_due)
        invoice.invoice_payment_term_id = self.payment_term_multi
        invoice.action_post()
        self.assertTrue(invoice.multi_due)
        self.assertEqual(len(invoice.multi_date_due.split()), 2)
        due_date = fields.date.today() + timedelta(days=60)
        lg = self.env["res.lang"]._lang_get(self.env.user.lang)
        locale = babel.Locale.parse(lg.code)
        babel_format = posix_to_ldml(lg.date_format, locale=locale)
        date_due_format = pycompat.to_text(
            babel.dates.format_date(due_date, format=babel_format, locale=locale)
        )
        res = (
            self.env["ir.actions.report"]
            ._get_report_from_name("account.report_invoice")
            .render_qweb_html(invoice.ids)
        )
        self.assertRegexpMatches(str(res[0]), date_due_format)
        self.assertRegexpMatches(str(res[0]), "75.0")
