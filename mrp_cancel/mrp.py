# -*- coding: utf-8 -*-



######################################################################
#
#  Note: Program metadata is available in /__init__.py
#
######################################################################

from openerp.osv import osv

class mrp_production(osv.osv): 
    _inherit = "mrp.production"

    def action_cancel(self, cr, uid, ids, context=None):

        """ OVERRIDE: to allow cancelling of MO and related picking in one step if picking is not completed.
        @return: status of super
        """
        if context is None:
            context = {}
        move_obj = self.pool.get('stock.move')
        stock_picking_obj = self.pool.get('stock.picking')
        for production in self.browse(cr, uid, ids, context=context):
            if production.state == 'confirmed' and production.picking_id.state == 'assigned':
                stock_picking_obj.write(cr, uid, [production.picking_id.id], {'state': 'cancel'})
                nids = move_obj.search(cr, uid, [ ('picking_id','=',production.picking_id.id) ] )
                move_obj.action_cancel(cr, uid, nids)
            if production.move_created_ids:
                move_obj.action_cancel(cr, uid, [x.id for x in production.move_created_ids]) 
            move_obj.action_cancel(cr, uid, [x.id for x in production.move_lines])
        
        return super(mrp_production, self).action_cancel(cr, uid, ids, context=context)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: