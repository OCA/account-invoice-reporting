# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from datetime import datetime, timedelta


invoice_fields = [
    'name',
    'type',
    'number',
    'state',
    'date_invoice',
    'date_due',
    'payment_ids'
]

payment_fields = [
    'name',
    'state',
    'date',
]


class res_partner(orm.Model):
    _inherit = 'res.partner'

    def _dtp_life(self, cr, uid, ids, name, arg, context=None):
        result = {}

        invoice_obj = self.pool.get('account.invoice')
        move_line_obj = self.pool.get('account.move.line')

        average_days_to_pay = 0
        for partner in ids:
            total_days_to_pay = 0
            inv_ids = invoice_obj.search(
                cr, uid, [('partner_id', '=', partner)]
            )
            total_number_of_invoices = 0
            for invoice in inv_ids:
                invoice_rec = invoice_obj.read(
                    cr, uid, invoice, invoice_fields, context=context
                )

                if (
                    invoice_rec['state'] == 'paid' and
                    invoice_rec['type'] == 'out_invoice'
                ):
                    total_number_of_invoices += 1
                    date_due = invoice_rec['date_invoice']
                    days_for_latest_payment = 0

                    for payment in invoice_rec['payment_ids']:
                        payment_rec = move_line_obj.read(
                            cr, uid, payment, payment_fields, context=context
                        )
                        if payment_rec['state'] == 'valid':
                            days_for_this_payment = (
                                datetime.strptime(
                                    payment_rec['date'], '%Y-%m-%d'
                                ) -
                                datetime.strptime(date_due, '%Y-%m-%d')
                            ).days

                            if days_for_this_payment < 0:
                                days_for_this_payment = 0
                            if days_for_this_payment > days_for_latest_payment:
                                days_for_latest_payment = days_for_this_payment

                    days_to_pay_invoice = days_for_latest_payment
                    total_days_to_pay = total_days_to_pay + days_to_pay_invoice
                    average_days_to_pay = (
                        total_days_to_pay / total_number_of_invoices
                    )

        result[partner] = average_days_to_pay
        return result

    def _dtp_ytd(self, cr, uid, ids, name, arg, context=None):
        result = {}

        invoice_obj = self.pool.get('account.invoice')
        move_line_obj = self.pool.get('account.move.line')

        average_days_to_pay = 0
        for partner in ids:
            total_days_to_pay = 0
            inv_ids = invoice_obj.search(
                cr, uid, [('partner_id', '=', partner)]
            )
            total_number_of_invoices = 0
            for invoice in inv_ids:
                invoice_rec = invoice_obj.read(
                    cr, uid, invoice, invoice_fields, context=context
                )

                if (
                    invoice_rec['state'] == 'paid' and
                    invoice_rec['type'] == 'out_invoice' and
                    (
                        datetime.strptime(
                            invoice_rec['date_invoice'], '%Y-%m-%d'
                        ).year == datetime.now().year
                    )
                ):
                    total_number_of_invoices += 1
                    date_due = invoice_rec['date_invoice']
                    days_for_latest_payment = 0

                    for payment in invoice_rec['payment_ids']:
                        payment_rec = move_line_obj.read(
                            cr, uid, payment, payment_fields, context=context
                        )

                        if payment_rec['state'] == 'valid':
                            days_for_this_payment = (
                                datetime.strptime(
                                    payment_rec['date'], '%Y-%m-%d'
                                ) - datetime.strptime(date_due, '%Y-%m-%d')
                            ).days

                            if days_for_this_payment < 0:
                                days_for_this_payment = 0
                            if days_for_this_payment > days_for_latest_payment:
                                days_for_latest_payment = days_for_this_payment

                    days_to_pay_invoice = days_for_latest_payment
                    total_days_to_pay = total_days_to_pay + days_to_pay_invoice
                    average_days_to_pay = (
                        total_days_to_pay / total_number_of_invoices
                    )

        result[partner] = average_days_to_pay
        return result

    def _dtr_life(self, cr, uid, ids, name, arg, context=None):
        result = {}

        invoice_obj = self.pool.get('account.invoice')
        move_line_obj = self.pool.get('account.move.line')

        average_days_to_pay = 0
        for partner in ids:
            total_days_to_pay = 0
            inv_ids = invoice_obj.search(
                cr, uid, [('partner_id', '=', partner)]
            )
            total_number_of_invoices = 0
            for invoice in inv_ids:
                invoice_rec = invoice_obj.read(
                    cr, uid, invoice, invoice_fields, context=context
                )

                if (
                    invoice_rec['state'] == 'paid' and
                    invoice_rec['type'] == 'in_invoice'
                ):
                    total_number_of_invoices += 1
                    date_due = invoice_rec['date_invoice']
                    days_for_latest_payment = 0

                    for payment in invoice_rec['payment_ids']:
                        payment_rec = move_line_obj.read(
                            cr, uid, payment, payment_fields, context=context
                        )
                        if payment_rec['state'] == 'valid':
                            days_for_this_payment = (
                                datetime.strptime(
                                    payment_rec['date'], '%Y-%m-%d'
                                ) - datetime.strptime(date_due, '%Y-%m-%d')
                            ).days

                            if days_for_this_payment < 0:
                                days_for_this_payment = 0
                            if days_for_this_payment > days_for_latest_payment:
                                days_for_latest_payment = days_for_this_payment

                    days_to_pay_invoice = days_for_latest_payment
                    total_days_to_pay = total_days_to_pay + days_to_pay_invoice
                    average_days_to_pay = (
                        total_days_to_pay / total_number_of_invoices
                    )

        result[partner] = average_days_to_pay
        return result

    def _dtr_ytd(self, cr, uid, ids, name, arg, context=None):
        result = {}

        invoice_obj = self.pool.get('account.invoice')
        move_line_obj = self.pool.get('account.move.line')

        average_days_to_pay = 0
        for partner in ids:
            total_days_to_pay = 0
            inv_ids = invoice_obj.search(
                cr, uid,
                [('partner_id', '=', partner)],
                context=context
            )
            total_number_of_invoices = 0

            for invoice in inv_ids:
                invoice_rec = invoice_obj.read(
                    cr, uid, invoice, invoice_fields, context=context
                )

                if (
                    invoice_rec['state'] == 'paid' and
                    invoice_rec['type'] == 'in_invoice' and
                    datetime.strptime(
                        invoice_rec['date_invoice'], '%Y-%m-%d'
                    ).year == datetime.now().year
                ):
                    total_number_of_invoices += 1
                    date_due = invoice_rec['date_invoice']
                    days_for_latest_payment = 0

                    for payment in invoice_rec['payment_ids']:
                        payment_rec = move_line_obj.read(
                            cr, uid, payment, payment_fields, context=context
                        )
                        if payment_rec['state'] == 'valid':
                            days_for_this_payment = (
                                datetime.strptime(
                                    payment_rec['date'], '%Y-%m-%d'
                                ) - datetime.strptime(date_due, '%Y-%m-%d')
                            ).days

                            if days_for_this_payment < 0:
                                days_for_this_payment = 0
                            if days_for_this_payment > days_for_latest_payment:
                                days_for_latest_payment = days_for_this_payment

                    days_to_pay_invoice = days_for_latest_payment
                    total_days_to_pay = total_days_to_pay + days_to_pay_invoice
                    average_days_to_pay = (
                        total_days_to_pay / total_number_of_invoices
                    )

        result[partner] = average_days_to_pay
        return result

    _columns = {
        'd2p_life': fields.function(
            _dtp_life,
            string='AVG Days to Pay (lifetime)',
            type='float',
            store=False
        ),
        'd2r_life': fields.function(
            _dtr_life,
            string='AVG Days to Pay (lifetime)',
            type='float',
            store=False
        ),
        'd2p_ytd': fields.function(
            _dtp_ytd,
            string='AVG Days to Pay (YTD)',
            type='float',
            store=False
        ),
        'd2r_ytd': fields.function(
            _dtr_ytd,
            string='AVG Days to Pay (YTD)',
            type='float',
            store=False
        ),
    }
