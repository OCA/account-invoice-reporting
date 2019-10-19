# Copyright 2014 Guewen Baconnier (Camptocamp SA)
# Copyright 2013-2014 Nicolas Bessi (Camptocamp SA)
# Copyright 2018 Vicent Cubells - Tecnativa
# Copyright 2019 Iván Todorovich (Druidoo)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    comment_template1_id = fields.Many2one(
        'base.comment.template',
        string='Top Comment Template',
        domain=[('position', '=', 'before_lines')],
    )

    comment_template2_id = fields.Many2one(
        'base.comment.template',
        string='Bottom Comment Template',
        domain=[('position', '=', 'after_lines')],
    )

    note1 = fields.Html('Top Comment')
    note2 = fields.Html('Bottom Comment')

    @api.onchange('comment_template1_id')
    def _set_note1(self):
        comment = self.comment_template1_id
        if comment:
            self.note1 = comment.get_value(self.partner_id.id)

    @api.onchange('comment_template2_id')
    def _set_note2(self):
        comment = self.comment_template2_id
        if comment:
            self.note2 = comment.get_value(self.partner_id.id)

    @api.onchange('partner_id', 'company_id')
    def _onchange_partner_id(self):
        res = super(AccountInvoice, self)._onchange_partner_id()
        comment_template = self.partner_id.property_comment_template_id
        if comment_template.position == 'before_lines':
            self.comment_template1_id = comment_template
        elif comment_template.position == 'after_lines':
            self.comment_template2_id = comment_template
        # Force note read when changing partner/company
        # to update to the current partner language.
        if self.comment_template1_id:
            self._set_note1()
        if self.comment_template2_id:
            self._set_note2()
        return res
