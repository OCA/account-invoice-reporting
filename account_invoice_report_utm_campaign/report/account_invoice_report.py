# Copyright (C) 2024 Akretion
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    campaign_id = fields.Many2one("utm.campaign", readonly=True)
    medium_id = fields.Many2one("utm.medium", readonly=True)
    source_id = fields.Many2one("utm.source", readonly=True)

    @api.model
    def _select(self):
        return super()._select() + (
            ", move.campaign_id AS campaign_id"
            ", move.medium_id AS medium_id"
            ", move.source_id AS source_id"
        )
