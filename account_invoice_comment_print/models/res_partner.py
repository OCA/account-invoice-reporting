#  Copyright 2023 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner (models.Model):
    _inherit = 'res.partner'

    invoice_print_comment = fields.Html(
        string="Comment to be printed in invoices",
    )
