from odoo import fields, models
from collections import defaultdict


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    dest_package_ids = fields.Many2many(
        comodel_name='stock.quant.package',
        compute='_compute_dest_packages',
        string="Destination Packages",
    )

    def _compute_dest_packages(self):
        for line in self:
            line.dest_package_ids = line.mapped(
                'move_line_ids.move_line_ids.result_package_id'
            )

    def packages_grouped_by_quantity(self):
        packages_dict = defaultdict(float)
        for sml in self.mapped('move_line_ids.move_line_ids'):
            packages_dict[sml.result_package_id.name] += sml.qty_done
        return packages_dict
