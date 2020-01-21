# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
#
##############################################################################
{
    'name': 'Account Reports',
    'version': '1.0',
    'sequence':1,
    'category': 'Account',
    'summary':'Generate Accoung Reports',
    'description': """

        This application will help to Generate Accounting Reports.
        
    """,
    'author': 'DevIntelle Consulting Service Pvt.Ltd', 
    'website': 'http://www.devintellecs.com',
    'depends': ['sale_stock','account_accountant','account_parent'],
    'data': [
        'views/res_company_views.xml',
        'wizard/dev_general_ledger_report_views.xml',
        'wizard/dev_balance_sheet_report_view.xml',
        'wizard/dev_profit_loss_report_views.xml',
        'report/general_ledger_report.xml',
        'report/balance_sheet_report.xml',
        'report/profit_loss_report.xml',
        'report/report_menu.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
