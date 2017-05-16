# -*- coding: utf-8 -*-
# © 2014 Guewen Baconnier (Camptocamp SA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{'name': 'Invoice Comments',
 'summary': 'Comments templates on invoice documents',
 'version': '9.0.1.0.0',
 'license': 'AGPL-3',
 'depends': ['account',
             'base_comment_template',
             ],
 'author': "Camptocamp,Odoo Community Association (OCA)",
 'data': ['views/account_invoice.xml',
          'views/base_comment_template.xml',
          'security/ir.model.access.csv',
          'views/report_invoice.xml',
          ],
 'category': 'Sale',
 'installable': True,
 }
