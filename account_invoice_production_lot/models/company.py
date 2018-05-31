# -*- coding: utf-8 -*-
# Copyright 2018 Nicola Malcontenti <nicola.malcontenti@agilebg.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    lot_use_date = fields.Boolean(
        'Adds Use Date for Production Lot on Invoice Line Report')


class AccountConfigSettings(models.TransientModel):
    _inherit = 'account.config.settings'

    lot_use_date = fields.Boolean(
        related='company_id.lot_use_date')
