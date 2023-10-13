# Copyright 2017 Carlos Dauden <carlos.dauden@tecnativa.com>
# Copyright 2018 David Vidal <david.vidal@tecnativa.com>
# Copyright 2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import html

from odoo import fields
from odoo.tests.common import Form, TransactionCase


class TestAccountInvoiceGroupPicking(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestAccountInvoiceGroupPicking, cls).setUpClass()
        cls.env = cls.env(
            context=dict(
                cls.env.context,
                mail_create_nolog=True,
                mail_create_nosubscribe=True,
                mail_notrack=True,
                no_reset_password=True,
                tracking_disable=True,
            )
        )
        cls.currency_usd = cls.env.ref("base.USD")
        cls.currency_usd.active = True
        # Make sure the currency of the company is USD, as this not always happens
        # To be removed in V17: https://github.com/odoo/odoo/pull/107113
        cls.company = cls.env.company
        cls.env.cr.execute(
            "UPDATE res_company SET currency_id = %s WHERE id = %s",
            [cls.env.ref("base.USD").id, cls.company.id],
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Product for test",
                "default_code": "TESTPROD01",
                "invoice_policy": "delivery",
            }
        )
        cls.service = cls.env["product.product"].create(
            {
                "name": "Test service product",
                "type": "service",
                "invoice_policy": "order",
            }
        )
        cls.service2 = cls.env["product.product"].create(
            {
                "name": "Test service product 2",
                "type": "service",
                "invoice_policy": "order",
            }
        )
        cls.partner = cls.env["res.partner"].create({"name": "Partner for test"})
        cls.sale = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": cls.product.name,
                            "product_id": cls.product.id,
                            "product_uom_qty": 2,
                            "product_uom": cls.product.uom_id.id,
                            "price_unit": 100.0,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": cls.service.name,
                            "product_id": cls.service.id,
                            "product_uom_qty": 3,
                            "product_uom": cls.service.uom_id.id,
                            "price_unit": 50.0,
                        },
                    ),
                ],
            }
        )
        cls.sale2 = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": cls.service2.name,
                            "product_id": cls.service2.id,
                            "product_uom_qty": 2,
                            "product_uom": cls.service2.uom_id.id,
                            "price_unit": 100.0,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": cls.service.name,
                            "product_id": cls.service.id,
                            "product_uom_qty": 3,
                            "product_uom": cls.service.uom_id.id,
                            "price_unit": 50.0,
                        },
                    ),
                ],
            }
        )

    def get_return_picking_wizard(self, picking):
        stock_return_picking_form = Form(
            self.env["stock.return.picking"].with_context(
                active_ids=picking.ids,
                active_id=picking.ids[0],
                active_model="stock.picking",
            )
        )
        return stock_return_picking_form.save()

    def test_account_invoice_group_picking(self):
        # confirm quotation
        self.sale.action_confirm()
        # deliver lines2
        self.sale.picking_ids[:1].action_confirm()
        self.sale.picking_ids[:1].move_line_ids.write({"qty_done": 1})
        self.sale.picking_ids[:1]._action_done()
        # create another sale
        self.sale2 = self.sale.copy()
        self.sale2.order_line[:1].product_uom_qty = 4
        self.sale2.order_line[:1].price_unit = 50.0
        # confirm new quotation
        self.sale2.action_confirm()
        self.sale2.picking_ids[:1].action_confirm()
        self.sale2.picking_ids[:1].move_line_ids.write({"qty_done": 1})
        self.sale2.picking_ids[:1]._action_done()
        sales = self.sale | self.sale2
        # invoice sales
        invoice = sales._create_invoices()
        # Test directly grouping method
        groups = invoice.lines_grouped_by_picking()
        self.assertEqual(len(groups), 4)
        self.assertEqual(groups[0]["picking"], groups[1]["picking"])
        self.assertEqual(groups[2]["picking"], groups[3]["picking"])
        # Test report
        content = html.document_fromstring(
            self.env.ref("account.account_invoices")._render_qweb_html(invoice.id)[0]
        )
        tbody = content.xpath("//tbody[@class='invoice_tbody']")
        tbody = [html.tostring(line, encoding="utf-8").strip() for line in tbody][
            0
        ].decode()
        # information about sales is printed
        self.assertEqual(tbody.count(self.sale.name), 1)
        self.assertEqual(tbody.count(self.sale2.name), 1)
        # information about pickings is printed
        self.assertTrue(self.sale.invoice_ids.picking_ids[:1].name in tbody)
        self.assertTrue(self.sale2.invoice_ids.picking_ids[:1].name in tbody)

    def test_account_invoice_group_picking_return(self):
        self.sale.action_confirm()
        # deliver lines2
        picking = self.sale.picking_ids[:1]
        picking.action_confirm()
        picking.move_line_ids.write({"qty_done": 1})
        picking._action_done()
        self.sale._create_invoices()
        # Return one picking from sale1
        wiz_return = self.get_return_picking_wizard(picking)
        res = wiz_return.create_returns()
        picking_return = self.env["stock.picking"].browse(res["res_id"])
        picking_return.move_line_ids.write({"qty_done": 1})
        picking_return._action_done()
        # Test directly grouping method
        invoice = self.sale._create_invoices(final=True)
        groups = invoice.lines_grouped_by_picking()
        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0]["picking"], picking_return)

    def test_account_invoice_return_without_returned_good(self):
        self.sale.action_confirm()
        picking = self.sale.picking_ids[:1]
        picking.action_confirm()
        picking.move_line_ids.write({"qty_done": 1})
        picking._action_done()
        invoice = self.sale._create_invoices()
        invoice.action_post()
        # Refund invoice without return picking
        move_reversal = (
            self.env["account.move.reversal"]
            .with_context(active_model="account.move", active_ids=invoice.ids)
            .create(
                {
                    "date": fields.Date.today(),
                    "reason": "no reason",
                    "refund_method": "refund",
                    "journal_id": invoice.journal_id.id,
                }
            )
        )
        reversal = move_reversal.reverse_moves()
        refund_invoice = self.env["account.move"].browse(reversal["res_id"])
        groups = refund_invoice.lines_grouped_by_picking()
        self.assertEqual(len(groups), 2)

    def test_account_invoice_group_picking_refund(self):
        # confirm quotation
        self.sale.action_confirm()
        # deliver lines2
        picking = self.sale.picking_ids[:1]
        picking.action_confirm()
        picking.move_line_ids.write({"qty_done": 1})
        picking._action_done()
        # invoice sales
        invoice = self.sale._create_invoices()
        invoice._post()
        # Test directly grouping method
        # invoice = self.env["account.move"].browse(inv_id)
        groups = invoice.lines_grouped_by_picking()
        self.assertEqual(len(groups), 2)
        self.assertEqual(groups[0]["picking"], groups[1]["picking"])
        # Test report
        content = html.document_fromstring(
            self.env.ref("account.account_invoices")._render_qweb_html(invoice.id)[0]
        )
        tbody = content.xpath("//tbody[@class='invoice_tbody']")
        tbody = [html.tostring(line, encoding="utf-8").strip() for line in tbody][
            0
        ].decode()
        # information about sales is printed
        self.assertEqual(tbody.count(self.sale.name), 1)
        # information about pickings is printed
        self.assertTrue(picking.name in tbody)
        # Return picking
        wiz_return = self.get_return_picking_wizard(picking)
        res = wiz_return.create_returns()
        picking_return = self.env["stock.picking"].browse(res["res_id"])
        picking_return.move_line_ids.write({"qty_done": 1})
        picking_return._action_done()
        # Refund invoice
        wiz_invoice_refund = (
            self.env["account.move.reversal"]
            .with_context(active_model="account.move", active_ids=invoice.ids)
            .create(
                {
                    "refund_method": "cancel",
                    "reason": "test",
                    "journal_id": invoice.journal_id.id,
                }
            )
        )
        wiz_invoice_refund.reverse_moves()
        new_invoice = self.sale.invoice_ids.filtered(
            lambda i: i.move_type == "out_refund"
        )
        # Test directly grouping method
        # invoice = self.env["account.move"].browse(inv_id)
        groups = new_invoice.lines_grouped_by_picking()
        self.assertEqual(len(groups), 2)
        self.assertEqual(groups[0]["picking"], groups[1]["picking"])
        # Test report
        content = html.document_fromstring(
            self.env.ref("account.account_invoices")._render_qweb_html(new_invoice.id)[
                0
            ]
        )
        tbody = content.xpath("//tbody[@class='invoice_tbody']")
        tbody = [html.tostring(line, encoding="utf-8").strip() for line in tbody][
            0
        ].decode()
        # information about sales is printed
        self.assertEqual(tbody.count(self.sale.name), 1)
        # information about pickings is printed
        self.assertTrue(picking_return.name in tbody)

    def test_account_invoice_group_picking_refund_without_return(self):
        # confirm quotation
        self.sale.action_confirm()
        # deliver lines2
        picking = self.sale.picking_ids[:1]
        picking.action_confirm()
        picking.move_line_ids.write({"qty_done": 1})
        picking._action_done()
        # invoice sales
        invoice = self.sale._create_invoices()
        invoice._post()
        # Test directly grouping method
        # invoice = self.env["account.move"].browse(inv_id)
        groups = invoice.lines_grouped_by_picking()
        self.assertEqual(len(groups), 2)
        self.assertEqual(groups[0]["picking"], groups[1]["picking"])
        # Test report
        content = html.document_fromstring(
            self.env.ref("account.account_invoices")._render_qweb_html(invoice.id)[0]
        )
        tbody = content.xpath("//tbody[@class='invoice_tbody']")
        tbody = [html.tostring(line, encoding="utf-8").strip() for line in tbody][
            0
        ].decode()
        # information about sales is printed
        self.assertEqual(tbody.count(self.sale.name), 1)
        # information about pickings is printed
        self.assertTrue(picking.name in tbody)
        # Refund invoice
        wiz_invoice_refund = (
            self.env["account.move.reversal"]
            .with_context(active_model="account.move", active_ids=invoice.ids)
            .create(
                {
                    "refund_method": "cancel",
                    "reason": "test",
                    "journal_id": invoice.journal_id.id,
                }
            )
        )
        wiz_invoice_refund.reverse_moves()
        new_invoice = self.sale.invoice_ids.filtered(
            lambda i: i.move_type == "out_refund"
        )
        # Test directly grouping method
        # invoice = self.env["account.move"].browse(inv_id)
        groups = new_invoice.lines_grouped_by_picking()
        self.assertEqual(len(groups), 2)
        self.assertEqual(groups[0]["picking"], groups[1]["picking"])
        # Test report
        content = html.document_fromstring(
            self.env.ref("account.account_invoices")._render_qweb_html(new_invoice.id)[
                0
            ]
        )
        tbody = content.xpath("//tbody[@class='invoice_tbody']")
        tbody = [html.tostring(line, encoding="utf-8").strip() for line in tbody][
            0
        ].decode()
        # information about sales is printed
        self.assertEqual(tbody.count(self.sale.name), 1)
        # information about pickings is printed
        self.assertTrue(picking.name in tbody)

    def test_account_invoice_group_picking_service_sale_reports_check(self):
        self.sale2.action_confirm()
        # invoice sales
        invoice = self.sale2._create_invoices()
        invoice._post()
        # Test report
        content = html.document_fromstring(
            self.env.ref("account.account_invoices")._render_qweb_html(invoice.id)[0]
        )
        tbody = content.xpath("//tbody[@class='invoice_tbody']")
        tbody = [html.tostring(line, encoding="utf-8").strip() for line in tbody][
            0
        ].decode()
        # check if service line is in report
        self.assertTrue(self.sale2.order_line[0].name in tbody)
        self.assertTrue(self.sale2.order_line[1].name in tbody)
        # Refund invoice
        wiz_invoice_refund = (
            self.env["account.move.reversal"]
            .with_context(active_model="account.move", active_ids=invoice.ids)
            .create(
                {
                    "refund_method": "cancel",
                    "reason": "test",
                    "journal_id": invoice.journal_id.id,
                }
            )
        )
        wiz_invoice_refund.reverse_moves()
        new_invoice = self.sale2.invoice_ids.filtered(
            lambda i: i.move_type == "out_refund"
        )
        # Test report
        content = html.document_fromstring(
            self.env.ref("account.account_invoices")._render_qweb_html(new_invoice.id)[
                0
            ]
        )
        tbody = content.xpath("//tbody[@class='invoice_tbody']")
        tbody = [html.tostring(line, encoding="utf-8").strip() for line in tbody][
            0
        ].decode()
        # check if service line is in report
        self.assertTrue(self.sale2.order_line[0].name in tbody)
        self.assertTrue(self.sale2.order_line[1].name in tbody)
