# Copyright 2017-2023 Tecnativa - Carlos Dauden
# Copyright 2018 Tecnativa - David Vidal
# Copyright 2018-2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import datetime
from collections import OrderedDict

from odoo import api, models
from odoo.tools import float_is_zero


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def _sort_grouped_lines(self, lines_dic):
        min_date = datetime.datetime.min
        return sorted(
            lines_dic,
            key=lambda x: (
                (
                    x["picking"].date or min_date,
                    x["picking"].date_done or x["picking"].date or min_date,
                )
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

    def _process_section_note_lines_grouped(
        self, previous_section, previous_note, lines_dic, pick_order=None
    ):
        key_section = (pick_order, previous_section) if pick_order else previous_section
        if previous_section and key_section not in lines_dic:
            lines_dic[key_section] = 0.0
        key_note = (pick_order, previous_note) if pick_order else previous_note
        if previous_note and key_note not in lines_dic:
            lines_dic[key_note] = 0.0

    def _get_grouped_by_picking_sorted_lines(self):
        return self.invoice_line_ids.sorted(
            lambda ln: (-ln.sequence, ln.date, ln.move_name, -ln.id), reverse=True
        )

    def lines_grouped_by_picking(self):
        """This prepares a data structure for printing the invoice report
        grouped by pickings."""
        self.ensure_one()
        picking_dict = OrderedDict()
        lines_dict = OrderedDict()
        picking_obj = self.env["stock.picking"]
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
        previous_section = previous_note = False
        sorted_lines = self._get_grouped_by_picking_sorted_lines()
        for line in sorted_lines:
            if line.display_type == "line_section":
                previous_section = line
                continue
            if line.display_type == "line_note":
                previous_note = line
                continue
            has_returned_qty = False
            remaining_qty = line.quantity
            for move in line.move_line_ids:
                key = (move.picking_id, line)
                self._process_section_note_lines_grouped(
                    previous_section, previous_note, picking_dict, move.picking_id
                )
                picking_dict.setdefault(key, 0)
                if move.location_id.usage == "customer":
                    has_returned_qty = True
                qty = self._get_signed_quantity_done(line, move, sign)
                picking_dict[key] += qty
                remaining_qty -= qty
            if not line.move_line_ids and line.sale_line_ids:
                for so_line in line.sale_line_ids:
                    if so_dict.get(so_line.order_id):
                        key = (so_dict[so_line.order_id], line)
                        self._process_section_note_lines_grouped(
                            previous_section,
                            previous_note,
                            picking_dict,
                            so_dict[so_line.order_id],
                        )
                        picking_dict.setdefault(key, 0)
                        qty = so_line.product_uom_qty
                        picking_dict[key] += qty
                        remaining_qty -= qty
            elif not line.move_line_ids and not line.sale_line_ids:
                key = (picking_obj, line)
                self._process_section_note_lines_grouped(
                    previous_section, previous_note, lines_dict
                )
                picking_dict.setdefault(key, 0)
                qty = line.quantity
                picking_dict[key] += qty
                remaining_qty -= qty
            # To avoid to print duplicate lines because the invoice is a refund
            # without returned goods to refund.
            if (
                self.move_type == "out_refund"
                and not has_returned_qty
                and remaining_qty
                and line.product_id.type != "service"
            ):
                remaining_qty = 0.0
                for key in picking_dict:
                    picking_dict[key] = abs(picking_dict[key])
            if not float_is_zero(
                remaining_qty,
                precision_rounding=line.product_id.uom_id.rounding or 0.01,
            ):
                lines_dict[line] = remaining_qty
        no_picking = [
            {"picking": picking_obj, "line": key, "quantity": value}
            for key, value in lines_dict.items()
        ]
        with_picking = [
            {"picking": key[0], "line": key[1], "quantity": value}
            for key, value in picking_dict.items()
        ]
        return no_picking + self._sort_grouped_lines(with_picking)
