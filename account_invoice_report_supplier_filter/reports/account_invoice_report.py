# Copyright 2020 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    seller_id = fields.Many2one(
        related='product_id.seller_ids.name',
        domain=[('supplier', '=', True)],
    )
