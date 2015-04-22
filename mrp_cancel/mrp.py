# -*- coding: utf-8 -*-
from openerp.osv import orm


class mrp_production(orm.Model):
    _inherit = "mrp.production"

    def action_cancel(self, cr, uid, ids, context=None):
        """
        Override action_cancel.

        OVERRIDE: to allow cancelling of MO and related picking in one step if
        picking is not completed.

        :return: status of super
        """
        if context is None:
            context = {}

        move_obj = self.pool.get('stock.move')
        stock_picking_obj = self.pool.get('stock.picking')

        for production in self.browse(cr, uid, ids, context=context):
            if (
                production.state == 'confirmed' and
                production.picking_id.state == 'assigned'
            ):
                stock_picking_obj.write(
                    cr, uid, [production.picking_id.id],
                    {'state': 'cancel'},
                    context=context
                )
                nids = move_obj.search(
                    cr, uid, [('picking_id', '=', production.picking_id.id)],
                    context=context
                )
                move_obj.action_cancel(cr, uid, nids, context=context)

            if production.move_created_ids:
                move_obj.action_cancel(
                    cr, uid,
                    [x.id for x in production.move_created_ids],
                    context=context
                )

            move_obj.action_cancel(
                cr, uid,
                [x.id for x in production.move_lines],
                context=context
            )

        base_func = super(mrp_production, self).action_cancel
        return base_func(cr, uid, ids, context=context)
