from openerp.osv import fields, osv

class CountryState(osv.osv):

    _description="State Counties"
    _name = 'res.country.state.county'

    _columns = {
        'state_id': fields.many2one('res.country.state', 'State',required=True),
        'name': fields.char('County', size=33, required=True,
                            help='United States second level administrative boundaries.'),
    }
    _order = 'state_id,name'
