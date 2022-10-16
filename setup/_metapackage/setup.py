import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-oca-account-invoice-reporting",
    description="Meta package for oca-account-invoice-reporting Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-account_comment_template',
        'odoo14-addon-account_invoice_line_report',
        'odoo14-addon-account_invoice_line_sale_line_position',
        'odoo14-addon-account_invoice_production_lot',
        'odoo14-addon-account_invoice_report_due_list',
        'odoo14-addon-account_invoice_report_grouped_by_picking',
        'odoo14-addon-account_invoice_report_grouped_by_picking_sale_mrp',
        'odoo14-addon-account_invoice_report_hide_line',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
