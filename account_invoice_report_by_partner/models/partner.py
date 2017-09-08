# -*- coding: utf-8 -*-
# Copyright 2014 Angel Moya <angel.moya@domatix.com>
# Copyright 2017 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    invoice_report_id = fields.Many2one(
        comodel_name='ir.actions.report.xml',
        string='Invoice Report Template',
        domain="[('model', '=', 'account.invoice')]",
    )
