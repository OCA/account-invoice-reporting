import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-account-invoice-reporting",
    description="Meta package for oca-account-invoice-reporting Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-account_comment_template>=16.0dev,<16.1dev',
        'odoo-addon-account_invoice_line_report>=16.0dev,<16.1dev',
        'odoo-addon-account_invoice_production_lot>=16.0dev,<16.1dev',
        'odoo-addon-account_invoice_report_due_list>=16.0dev,<16.1dev',
        'odoo-addon-account_invoice_report_grouped_by_picking>=16.0dev,<16.1dev',
        'odoo-addon-account_invoice_report_payment_info>=16.0dev,<16.1dev',
        'odoo-addon-account_reporting_volume>=16.0dev,<16.1dev',
        'odoo-addon-account_reporting_weight>=16.0dev,<16.1dev',
        'odoo-addon-partner_time_to_pay>=16.0dev,<16.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 16.0',
    ]
)
