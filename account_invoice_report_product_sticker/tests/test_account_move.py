# Copyright 2025 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from .common import ProductStickerInvoiceReportCommon


class TestStickersOnAccountInvoice(ProductStickerInvoiceReportCommon):
    def test_invoices(self):
        target_product = self.product_as400.product_variant_ids[0]
        product_stickers = target_product.get_product_stickers()
        out_invoice = self._create_invoice(
            "out_invoice", [target_product, target_product]
        )
        self.assertEqual(
            out_invoice.show_product_stickers,
            self.default_sticker_position,
            "Out Invoice should show stickers",
        )
        self.assertEqual(
            out_invoice.sticker_ids,
            product_stickers,
            "(Out Invoice) Not the same images than the product",
        )
        out_refund = self._create_invoice(
            "out_refund", [target_product, target_product]
        )
        self.assertEqual(
            out_refund.show_product_stickers,
            self.default_sticker_position,
            "Out Refund should show stickers",
        )
        self.assertEqual(
            out_refund.sticker_ids,
            product_stickers,
            "(Out Refund) Not the same images than the product",
        )
        in_invoice = self._create_invoice(
            "in_invoice", [target_product, target_product]
        )
        self.assertFalse(
            in_invoice.show_product_stickers,
            "In Invoice should not show stickers",
        )
        self.assertFalse(
            in_invoice.sticker_ids,
            "(In Invoice) Should not have stickers",
        )
