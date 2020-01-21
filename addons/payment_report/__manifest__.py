# -*- coding: utf-8 -*-
{
    'name': 'Pago Entry Report',
    'version': '1.1',
    'author': 'Odoo',
    'summary': 'Print a particular Journal Entry',
    'description': """  """,
    'category': 'Accounting',
    'website': 'http://odoo.org.bo/',

    'depends': ['base', 'account_accountant',
                ],

    'data': [
        'views/report_journal_entry2.xml'
    ],

    'qweb': [],
    'images': ['static/description/iWesabe-Apps-Journal-Entry-Report.png'],

    'installable': True,
    'application': True,
    'auto_install': False,
}
