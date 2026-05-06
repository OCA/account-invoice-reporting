# © 2026 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


from odoo.fields import Command
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestStockMoveWarehouseView(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.product_template = cls.env["product.template"].create(
            {
                "name": "Producto Test",
                "type": "consu",
            }
        )
        cls.product = cls.product_template.product_variant_id

        cls.secondary_unit_box = cls.env["product.secondary.unit"].create(
            {
                "name": "Caja 10",
                "factor": 10.0,
                "product_tmpl_id": cls.product_template.id,
                "uom_id": cls.product_template.uom_id.id,
            }
        )

        cls.secondary_unit_pallet = cls.env["product.secondary.unit"].create(
            {
                "name": "Pallet 100",
                "factor": 100.0,
                "product_tmpl_id": cls.product_template.id,
                "uom_id": cls.product_template.uom_id.id,
            }
        )

        cls.product_template.sale_secondary_uom_id = cls.secondary_unit_box.id

        cls.partner = cls.env["res.partner"].create({"name": "Cliente Test"})

    def test_01_fallback_to_product_unit(self):
        invoice = self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": self.partner.id,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "product_id": self.product.id,
                            "quantity": 50.0,
                        }
                    )
                ],
            }
        )
        line = invoice.invoice_line_ids[0]

        self.assertEqual(line.secondary_uom_id, self.secondary_unit_box)
        self.assertAlmostEqual(line.secondary_uom_qty, 5.0)

    def test_02_priority_sale_line(self):
        sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": self.product.id,
                            "product_uom_qty": 200.0,
                            "secondary_uom_id": self.secondary_unit_pallet.id,
                        }
                    )
                ],
            }
        )
        sale_order.action_confirm()

        invoice = sale_order._create_invoices()

        if isinstance(invoice, dict):
            invoice = self.env["account.move"].browse(invoice.get("res_id"))

        line = invoice.invoice_line_ids.filtered(lambda x: x.display_type == "product")[
            :1
        ]

        self.assertEqual(line.secondary_uom_id, self.secondary_unit_pallet)
        self.assertAlmostEqual(line.secondary_uom_qty, 2.0)

    def test_03_manual_change(self):
        invoice = self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": self.partner.id,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "product_id": self.product.id,
                            "quantity": 100.0,
                        }
                    )
                ],
            }
        )
        line = invoice.invoice_line_ids[0]
        self.assertEqual(line.secondary_uom_qty, 10.0)

        line.quantity = 250.0
        line._compute_secondary_uom_id()

        self.assertEqual(line.secondary_uom_qty, 25.0)
