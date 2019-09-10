import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-oca-account-invoice-reporting",
    description="Meta package for oca-account-invoice-reporting Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-account_invoice_comment_template',
        'odoo12-addon-account_invoice_line_report',
        'odoo12-addon-account_invoice_report_due_list',
        'odoo12-addon-account_invoice_report_hide_line',
        'odoo12-addon-base_comment_template',
        'odoo12-addon-partner_time_to_pay',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
