# -*- coding: utf-8 -*-

######################################################################
#
#  Note: Program metadata is available in /__init__.py
#
######################################################################

{
    "name" : "United States - States & Counties",
    "version" : "1.7",
    "author" : "Ursa Information Systems",
    "summary": "Add missing states, add US county equivalents with filter (Ursa).",
    'description':
        """
Based on US Census information (updated 2014) - adds a dropdown list on the partner form view, filtered by state.  In some states, sales tax rates are based on Counties.  For those where this is the case, this module could be used in conjunction with rules to determine sales tax.

        """,
    'maintainer': 'Ursa Information Systems',
    'website': 'http://www.ursainfosystems.com',
    "category" : "Localization",
    "images" : [],
    "depends" : ["base", ],
    "init_xml" : [],
    "demo_xml" : [],
    "data" : [
        'view/res_partner.xml',
        'view/res_country.xml',
        'data/res.country.state.csv',
        'data/res.country.state.county.csv',
        'data/ir.model.access.csv',
    ],
    "test" : [
    ],
    "auto_install": False,
    "application": False,
    "installable": True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
