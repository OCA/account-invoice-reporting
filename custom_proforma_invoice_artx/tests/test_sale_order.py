# tests/test_sale_order.py

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestSaleOrder(TransactionCase):
    def setUp(self):
        super().setUp()
        self.SaleOrder = self.env["sale.order"]
        self.partner = self.env["res.partner"].create({"name": "Test Partner"})
        self.product = self.env["product.product"].create(
            {
                "name": "Test Product",
                "type": "consu",
                "list_price": 100.0,
            }
        )

    def test_valid_down_payment_write(self):
        sale_order = self.SaleOrder.create(
            {
                "partner_id": self.partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "product_uom_qty": 1,
                            "price_unit": 100.0,
                        },
                    )
                ],
            }
        )

        # Valid down payment (should pass)
        sale_order.write({"down_payment": 50.0})
        self.assertEqual(sale_order.down_payment, 50.0)

    def test_invalid_down_payment_write(self):
        sale_order = self.SaleOrder.create(
            {
                "partner_id": self.partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "product_uom_qty": 1,
                            "price_unit": 100.0,
                        },
                    )
                ],
            }
        )

        # Invalid down payment (should raise error)
        with self.assertRaises(ValidationError):
            sale_order.write({"down_payment": 150.0})
