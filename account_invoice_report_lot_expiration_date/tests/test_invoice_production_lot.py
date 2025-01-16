# Copyright 2025 Binhex - Adasat Torres de León
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from datetime import date

from freezegun import freeze_time

from odoo.tests.common import TransactionCase, tagged
from odoo.tools.misc import format_date

_logger = logging.getLogger(__name__)


@freeze_time("2025-01-01")
@tagged("post_install", "-at_install")
class TestProdLot(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.warehouse = cls.env["stock.warehouse"].search(
            [("company_id", "=", cls.env.company.id)], limit=1
        )
        cls.lang = cls.env["res.lang"]._lang_get(cls.env.lang or cls.env.user.lang)
        cls.partner = cls.env["res.partner"].create(
            {"name": "Test partner", "lang": cls.env.lang}
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Product Test",
                "type": "product",
                "tracking": "lot",
                "invoice_policy": "delivery",
                "list_price": 15,
                "use_expiration_date": True,
                "expiration_time": 30,
            }
        )

        cls.lot = cls.env["stock.lot"].create(
            {
                "name": "Lot 1",
                "product_id": cls.product.id,
                "company_id": cls.company.id,
            }
        )

        cls.env["stock.quant"]._update_available_quantity(
            cls.product, cls.warehouse.lot_stock_id, 10, lot_id=cls.lot
        )

        cls.so = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": cls.product.name,
                            "product_id": cls.product.id,
                            "product_uom_qty": 1,
                        },
                    )
                ],
            }
        )
        cls.so.action_confirm()
        cls.pickings = cls.so.picking_ids
        cls.pickings.move_ids.quantity_done = 1
        cls.pickings.move_ids.write({"lot_ids": [(4, cls.lot.id)]})
        cls.pickings.button_validate()

        cls.invoice = cls.so._create_invoices()
        cls.invoice.action_post()

    def test_get_invoiced_lot_values(self):
        lot_values = self.invoice.sudo()._get_invoiced_lot_values()
        self.assertEqual(len(lot_values), 1)
        self.assertEqual(
            lot_values[0]["expiration_date"], format_date(self.env, date(2025, 1, 31))
        )
