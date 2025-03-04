# Copyright 2025 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo.tests import new_test_user, tagged

from odoo.addons.product_sticker.tests.common import ProductStickerCommon

from ..models.res_config_settings import REPORT_STICKER_POSITIONS


@tagged("post_install", "-at_install")
class ProductStickerInvoiceReportCommon(ProductStickerCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Test Partner"})
        cls.default_sticker_position = REPORT_STICKER_POSITIONS[0][0]
        cls.env["ir.config_parameter"].sudo().set_param(
            "account_invoice_report_product_sticker.show_product_stickers",
            cls.default_sticker_position,
        )
        cls.env = cls.env(
            user=new_test_user(
                cls.env, "test_accountant", groups="account.group_account_invoice"
            )
        )

    def _create_invoice(self, move_type, products):
        return self.env["account.move"].create(
            {
                "partner_id": self.partner.id,
                "move_type": move_type,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": product.id,
                            "quantity": 1,
                            "price_unit": 1,
                        },
                    )
                    for product in products
                ],
            }
        )
