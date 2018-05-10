# -*- coding: utf-8 -*-
# Copyright 2014 Guewen Baconnier (Camptocamp SA)
# Copyright 2013-2014 Nicolas Bessi (Camptocamp SA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{'name': 'Invoice Comments',
 'summary': 'Comments templates on invoice documents',
 'version': '10.0.1.1.0',
 'depends': ['account',
             'base_comment_template',
             ],
 'author': "Camptocamp,Odoo Community Association (OCA)",
 "license": "AGPL-3",
 'data': ['views/account_invoice_view.xml',
          'views/base_comment_template_view.xml',
          'security/ir.model.access.csv',
          'views/report_invoice.xml',
          'views/res_partner_views.xml',
          ],
 'category': 'Sale',
 'installable': True,
 }
