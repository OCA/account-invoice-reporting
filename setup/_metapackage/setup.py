import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo11-addons-oca-account-invoice-reporting",
    description="Meta package for oca-account-invoice-reporting Odoo addons",
    version=version,
    install_requires=[
        'odoo11-addon-account_invoice_comment_template',
        'odoo11-addon-account_invoice_line_report',
        'odoo11-addon-account_invoice_report_grouped_by_picking',
        'odoo11-addon-base_comment_template',
        'odoo11-addon-partner_time_to_pay',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
