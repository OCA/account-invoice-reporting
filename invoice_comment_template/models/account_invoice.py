# -*- coding: utf-8 -*-
# Copyright 2014 Guewen Baconnier (Camptocamp SA)
# Copyright 2013-2014 Nicolas Bessi (Camptocamp SA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    comment_template1_id = fields.Many2one('base.comment.template',
                                           string='Top Comment Template')
    comment_template2_id = fields.Many2one('base.comment.template',
                                           string='Bottom Comment Template')
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
