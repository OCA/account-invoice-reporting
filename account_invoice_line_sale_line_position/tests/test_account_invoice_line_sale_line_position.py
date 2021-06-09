# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo.tests import SingleTransactionCase


class TestAccountInvoiceLineSaleLinePosition(SingleTransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.partner = cls.env.ref("base.res_partner_12")
        cls.product = cls.env.ref("product.product_product_9")
        cls.order = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product.id,
                            "name": cls.product.name,
                            "product_uom_qty": 4.0,
                            "price_unit": 123.0,
                            "qty_delivered": 4.0,
                        },
                    ),
                    (0, 0, {"name": "section", "display_type": "line_section"},),
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product.id,
                            "name": cls.product.name,
                            "product_uom_qty": 1.0,
                            "price_unit": 0.0,
                            "qty_delivered": 1.0,
                        },
                    ),
                ],
            }
        )
        cls.order.action_confirm()
        cls.order._force_lines_to_invoice_policy_order()

    def test_invoice_position(self):
        """Check positions are retrieved from sale line."""
        self.invoice = self.order._create_invoices()
        self.assertEqual(self.invoice.invoice_line_ids[0].position_formatted, "001")
        self.assertEqual(self.invoice.invoice_line_ids[1].position_formatted, "")
        self.assertEqual(self.invoice.invoice_line_ids[2].position_formatted, "002")
