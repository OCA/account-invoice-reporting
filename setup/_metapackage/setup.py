import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo9-addons-oca-account-invoice-reporting",
    description="Meta package for oca-account-invoice-reporting Odoo addons",
    version=version,
    install_requires=[
        'odoo9-addon-account_draft_invoice_print',
        'odoo9-addon-account_invoice_line_report',
        'odoo9-addon-account_reporting_weight',
        'odoo9-addon-base_comment_template',
        'odoo9-addon-invoice_comment_template',
        'odoo9-addon-product_brand_invoice_report',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 9.0',
    ]
)
