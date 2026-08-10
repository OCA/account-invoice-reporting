# Copyright 2026 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    account_move_hidden_report_tax = fields.Boolean(
        related="company_id.account_move_hidden_report_tax", readonly=False
    )
