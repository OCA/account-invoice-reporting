import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-account-invoice-reporting",
    description="Meta package for oca-account-invoice-reporting Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-account_comment_template>=15.0dev,<15.1dev',
        'odoo-addon-account_invoice_line_sale_line_position>=15.0dev,<15.1dev',
        'odoo-addon-account_invoice_report_due_list>=15.0dev,<15.1dev',
        'odoo-addon-account_invoice_report_payment_info>=15.0dev,<15.1dev',
        'odoo-addon-account_reporting_weight>=15.0dev,<15.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 15.0',
    ]
)
