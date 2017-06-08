# -*- coding: utf-8 -*-
from openerp.osv import orm, fields


class res_partner(orm.Model):

    _inherit = "res.partner"

    _columns = {
        'county_id': fields.many2one("res.country.state.county", 'County'),
    }
