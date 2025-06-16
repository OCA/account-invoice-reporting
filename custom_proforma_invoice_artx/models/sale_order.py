# models/sale_order.py
# mohammad change add stage in sale order
from odoo import models, fields, api, exceptions


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    down_payment = fields.Monetary(string='Down Payment For Profoma Invoice', currency_field='currency_id')

    def write(self, vals):
        if 'down_payment' in vals:
            new_down_payment = vals.get('down_payment', 0.0)
            for order in self:
                if new_down_payment > order.amount_total:
                    raise exceptions.ValidationError("Down payment cannot exceed the total order amount.")
        return super(SaleOrder, self).write(vals)
