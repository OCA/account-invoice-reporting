#  Copyright 2023 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountInvoice (models.Model):
    _inherit = 'account.invoice'

    print_comment = fields.Html(
        string="Comment to be printed",
    )

    @api.onchange(
        'partner_id',
    )
    def _onchange_partner_print_comment(self):
        """Propagate print comment from selected partner to `self`."""
        self.ensure_one()
        partner = self.partner_id
        if partner:
            self.print_comment = partner.invoice_print_comment
