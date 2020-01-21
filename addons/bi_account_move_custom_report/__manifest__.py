# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Account Move Report Customization',
    'version': '10.0.0.2',
    'sequence': 4,
    'summary': 'Account Move Report Customization',
    'category' : 'Account',
    'description': """

	Account Move Report Customization
    """,
    'author': 'BrowseInfo',
    'website': 'https://browseinfo.in/',
    'depends': ['base', 'sale', 'account', 'account_accountant', 'stock'],
    'data': [
             "views/account_move.xml",
             "data/account_demo.xml",
             "report/account_move_report_wizard_view.xml",
             "report/account_move_report_view.xml",
             "report/account_move_report_template_view.xml",
             
             ],
	'qweb': [
		],
    'demo': [],
    'test': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images':['static/description/Banner.png'],
}


#	account.move ni create method ma lakhvanu k jo field ma value na hy to sequence generate karavani and jo hy to prefix and post fix add karavani
