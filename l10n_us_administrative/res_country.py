# -*- coding: utf-8 -*-
from openerp.osv import fields, orm


class CountryState(orm.Model):

    _description = "State Counties"
    _name = 'res.country.state.county'

    _columns = {
        'state_id': fields.many2one(
            'res.country.state',
            'State',
            required=True
        ),
        'name': fields.char(
            'County',
            required=True,
            help='United States second level administrative boundaries.'
        ),
    }

    _order = 'state_id,name'
