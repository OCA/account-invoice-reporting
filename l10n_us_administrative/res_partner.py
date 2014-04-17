from openerp.osv import osv, fields

class res_partner(osv.osv):

    _inherit = "res.partner"

    _columns = {
        'county_id': fields.many2one("res.country.state.county", 'County'),
    }

