# Copyright 2014 Guewen Baconnier (Camptocamp SA)
# Copyright 2013-2014 Nicolas Bessi (Camptocamp SA)
# Copyright 2018 Vicent Cubells - Tecnativa
# Copyright 2019 Iván Todorovich (Druidoo)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountMove(models.Model):
    """Add text comment"""

    _inherit = ["account.move", "comment.template"]
    _name = "account.move"
