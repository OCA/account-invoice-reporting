import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo10-addons-oca-account-invoice-reporting",
    description="Meta package for oca-account-invoice-reporting Odoo addons",
    version=version,
    install_requires=[
        'odoo10-addon-account_draft_invoice_print',
        'odoo10-addon-account_invoice_line_report',
        'odoo10-addon-account_invoice_production_lot',
        'odoo10-addon-account_invoice_report_by_partner',
        'odoo10-addon-base_comment_template',
        'odoo10-addon-invoice_comment_template',
        'odoo10-addon-partner_daytopay',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
