# -*- coding: utf-8 -*-
#
#
#    Authors: Damien Crier
#    Copyright 2015 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

from openerp import fields, exceptions
from openerp.tests import common


class TestInvoice(common.TransactionCase):

    def setUp(self):
        super(TestInvoice, self).setUp()
        self.inv_model = self.env['account.invoice']
        self.condition_text_obj = self.env['account.condition_text']
        self.partner_2 = self.env.ref('base.res_partner_2')

        self.condition1 = self.condition_text_obj.create(
            {'name': 'header',
             'type': 'header',
             'text': 'text header'
             }
            )

    def test_set_condition_no_commentid(self):
        self.assertEqual({},
                         self.inv_model._set_condition(0, 0, 0,
                                                       partner_id=False)
                         )

    def test_set_condition_no_partner(self):
        with self.assertRaises(exceptions.except_orm):
            self.inv_model._set_condition(0, 10, 0, partner_id=False)

    def test_condition(self):
        res = self.inv_model._set_condition(
            0, self.condition1.id, "key_test", partner_id=self.partner_2.id)
        self.assertEqual(self.condition1.text, res['value']['key_test'])

    def test_set_header(self):
        res = self.inv_model.set_header(0, self.condition1.id,
                                        partner_id=self.partner_2.id)
        self.assertEqual(self.condition1.text, res['value']['note1'])

    def test_set_footer(self):
        res = self.inv_model.set_footer(0, self.condition1.id,
                                        partner_id=self.partner_2.id)
        self.assertEqual(self.condition1.text, res['value']['note2'])
