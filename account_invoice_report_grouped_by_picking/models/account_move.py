# Copyright 2017 Tecnativa - Carlos Dauden
# Copyright 2018 Tecnativa - David Vidal
# Copyright 2018-2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from collections import OrderedDict

from odoo import api, fields, models
from odoo.tools import float_is_zero


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def _sort_grouped_lines(self, lines_dic):
        return sorted(
            lines_dic,
            key=lambda x: (
                (x["picking"].date, x["picking"].date_done or x["picking"].date)
            ),
        )

    def _get_signed_quantity_done(self, invoice_line, move, sign):
        """Hook method. Usage example:
        account_invoice_report_grouped_by_picking_sale_mrp module
        """
        qty = 0
        if move.location_id.usage == "customer":
            qty = -move.quantity_done * sign
        elif move.location_dest_id.usage == "customer":
            qty = move.quantity_done * sign
        return qty

    def lines_grouped_by_picking(self):
        """This prepares a data structure for printing the invoice report
        grouped by pickings."""
        self.ensure_one()
        picking_dict = OrderedDict()
        lines_dict = OrderedDict()
        # Not change sign if the credit note has been created from reverse move option
        # and it has the same pickings related than the reversed invoice instead of sale
        # order invoicing process after picking reverse transfer
        sign = (
            -1.0
            if self.move_type == "out_refund"
            and (
                not self.reversed_entry_id
                or self.reversed_entry_id.picking_ids != self.picking_ids
            )
            else 1.0
        )
        # Let's get first a correspondance between pickings and sales order
        so_dict = {x.sale_id: x for x in self.picking_ids if x.sale_id}
        # Now group by picking by direct link or via same SO as picking's one
        for line in self.invoice_line_ids.filtered(lambda x: not x.display_type):
            has_returned_qty = False
            remaining_qty = line.quantity
            for move in line.move_line_ids:
                key = (move.picking_id, line)
                picking_dict.setdefault(key, 0)
                qty = self._get_signed_quantity_done(line, move, sign)
                picking_dict[key] += qty
                remaining_qty -= qty
            if not line.move_line_ids and line.sale_line_ids:
                for so_line in line.sale_line_ids:
                    if so_dict.get(so_line.order_id):
                        key = (so_dict[so_line.order_id], line)
                        picking_dict.setdefault(key, 0)
                        qty = so_line.product_uom_qty
                        picking_dict[key] += qty
                        remaining_qty -= qty
            elif not line.move_line_ids and not line.sale_line_ids:
                key = (self.env["stock.picking"], line)
                picking_dict.setdefault(key, 0)
                qty = line.quantity
                picking_dict[key] += qty
                remaining_qty -= qty
            # To avoid to print duplicate lines because the invoice is a refund
            # without returned goods to refund.
            if self.move_type == "out_refund" and not has_returned_qty:
                remaining_qty = 0.0
                for key in picking_dict:
                    picking_dict[key] = abs(picking_dict[key])
            if not float_is_zero(
                remaining_qty,
                precision_rounding=line.product_id.uom_id.rounding or 0.01,
            ):
                lines_dict[line] = remaining_qty
        no_picking = [
            {"picking": False, "line": key, "quantity": value}
            for key, value in lines_dict.items()
        ]
        with_picking = [
            {"picking": key[0], "line": key[1], "quantity": value}
            for key, value in picking_dict.items()
        ]
        return no_picking + self._sort_grouped_lines(with_picking)
