{
    'name': 'Sale Proforma Custom Amount',
    'summary': 'Generate proforma invoices with custom down payment amount in Sale Orders.',
    'version': '17.0.1.0.0',  # OCA versioning: <Odoo Version>.<Major>.<Minor>.<Patch>
    'category': 'Sales',
    'author': 'Areterix Technologies',
    'website': 'https://areterix.com',
    'license': 'LGPL-3',
    'depends': [
        'sale',
    ],
    'data': [
        'views/sale_order_views.xml',
        'report/report_proforma_invoice_template.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,  # Set to False for OCA unless it's a complete application
    'auto_install': False,
    'development_status': 'Beta',
    'maintainers': ['umaniar-plus'],  # Your OCA GitHub username here
}
