# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
#    Globalteckz Software Solutions and Services                             #
#    Copyright (C) 2013-Today(www.globalteckz.com).                          #
#                                                                            #
#    This program is free software: you can redistribute it and/or modify    #
#    it under the terms of the GNU Affero General Public License as          #
#    published by the Free Software Foundation, either version 3 of the      #
#    License, or (at your option) any later version.                         #
#                                                                            #
#    This program is distributed in the hope that it will be useful,         #  
#    but WITHOUT ANY WARRANTY; without even the implied warranty of          #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
#    GNU Affero General Public License for more details.                     #
#                                                                            #
#                                                                            #
##############################################################################

{
    'name': 'Stock valuation report on particular date in pdf and xls',
    'version': '1.0',
    'category': 'Generic Modules',
    'sequence': 1,
    'author': 'Globalteckz',
    "category": "Website",
    'website': 'http://www.globalteckz.com',
    'summary': 'Odoo stock valuation between or particular dates in pdf and xls format',
    'description': """

Odoo Stock Valuation On Date

--------------------------------------------
Some of the feature of the module:
--------------------------------------------

1. Past Date Valuation,
2. Working with all Standard, Average and Real Price Methods,
3. Price comparision with old dates,
4. Filter By Product Categories,
5. Total summary By Dates,

------------------------------------------------------------------------------

    """,
    'depends': ['sale','stock','base'],
    'data': [
            'security/inventory_value_secure.xml',
            'security/ir.model.access.csv',
            'wizard/inventory_value_view.xml',
            'views/inventory_value_report.xml',
            'report/inventory_valuation_tmpl.xml',
            ],
    'application': True,
    'installable': True,
    'auto_install': False,
}
