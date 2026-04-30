# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import Command

from odoo.addons.base.tests.common import BaseCommon


class TestAccountInvoiceLineSaleLinePosition(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env["product.product"].create(
            {"name": "Test Product", "type": "consu"}
        )
        cls.order = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": cls.product.id,
                            "name": cls.product.name,
                            "product_uom_qty": 4.0,
                            "price_unit": 123.0,
                            "qty_delivered": 4.0,
                        },
                    ),
                    Command.create(
                        {"name": "section", "display_type": "line_section"},
                    ),
                    Command.create(
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
