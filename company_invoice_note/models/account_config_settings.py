# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models, _


class AccountConfigSettings(models.TransientModel):
    _inherit = 'account.config.settings'

    @api.model
    def _get_selection_invoice_note_place(self):
        """
        Get all possible selection choice (for invoice_note_place field)
        This list depends on values set on res.company.
        Returns: list of tuple (str, str)
        """
        fields_get = self.env['res.company'].fields_get(
            allfields=['invoice_note_place'])
        values = [
            (v[0], _(v[1])) for v in fields_get.get(
                'invoice_note_place', {}).get('selection', '')
        ]
        return values

    invoice_note_place = fields.Selection(
        selection=_get_selection_invoice_note_place,
        default="no",
        required=True,
        help="Define on where to place the additional invoice note on the "
             "invoice report",
        related="company_id.invoice_note_place",
    )
    invoice_note = fields.Html(
        help="Note who'll be printed on every invoice related to this company",
        related="company_id.invoice_note",
    )
