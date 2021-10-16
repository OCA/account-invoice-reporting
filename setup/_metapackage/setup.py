import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo8-addons-oca-account-invoice-reporting",
    description="Meta package for oca-account-invoice-reporting Odoo addons",
    version=version,
    install_requires=[
        'odoo8-addon-account_draft_invoice_print',
        'odoo8-addon-account_invoice_picking_address',
        'odoo8-addon-account_invoice_production_lot',
        'odoo8-addon-account_invoice_report_by_partner',
        'odoo8-addon-base_comment_template',
        'odoo8-addon-invoice_comment_template',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 8.0',
    ]
)
