import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo13-addons-oca-account-invoice-reporting",
    description="Meta package for oca-account-invoice-reporting Odoo addons",
    version=version,
    install_requires=[
        'odoo13-addon-account_invoice_line_report',
        'odoo13-addon-account_invoice_production_lot',
        'odoo13-addon-account_invoice_report_due_list',
        'odoo13-addon-account_invoice_report_grouped_by_picking',
        'odoo13-addon-account_reporting_weight',
        'odoo13-addon-partner_time_to_pay',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
