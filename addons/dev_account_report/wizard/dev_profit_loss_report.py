# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
#
##############################################################################

from odoo import api, fields, models, _
from datetime import date
from dateutil.relativedelta import relativedelta

import itertools
from operator import itemgetter
import operator

class dev_profit_loss_report(models.TransientModel):
    _name = "dev.profit.loss.report"
    
    
    @api.model
    def get_start_date(self):
        today = date.today()
        start_date = today.replace(day=1)
        return start_date
    
    @api.model
    def get_end_date(self):
        today = date.today()
        end_date = today + relativedelta(day=1, months=+1, days=-1)
        return end_date
        
    
    start_date = fields.Date('Start Date', default=get_start_date, required="1")
    end_date = fields.Date('End Date', default=get_end_date, required="1")
    company_id = fields.Many2one('res.company', default=lambda self:self.env.user.company_id)
    target_moves = fields.Selection([('all','All Entries'),('posted','All Posted Entries')], default='posted', string='Target Moves')
    
    is_comparison = fields.Boolean('Comparison')
    com_start_date = fields.Date('Start Date')
    com_end_date =  fields.Date('End Date')
    
    
    @api.multi
    def print_profit_loss_report(self):
        return self.env['report'].get_action(self,'dev_account_report.dev_profit_loss_report')
        
    
    @api.multi
    def get_parent_account(self):
        if self.company_id.profit_loss_account_ids:
            account_ids = self.env['account.account'].with_context({'show_parent_account':True}).search([('id','in',self.company_id.profit_loss_account_ids.ids)],order='code')
            return account_ids
        return False
            
    
    @api.multi
    def get_lines(self):
        account_ids = self.get_parent_account()
        final_lst = []
        count = 0
        if account_ids:
            for account in account_ids:
                lst = []
                count +=1
                balance = account.with_context({'date_from':self.start_date, 'date_to':self.end_date,'strict_range':True}).balance
                com_balance = account.with_context({'date_from':self.com_start_date, 'date_to':self.com_end_date,'strict_range':True}).balance
                lst.append({
                    'x_name':'',
                    'name':account.code + ' '+ account.name,
                    'seq':count,
                    'is_bold':True,
                    'balance':balance,
                    'com_balance':com_balance,
                })
                count +=1
                for child_1 in account.with_context({'show_parent_account':True}).child_ids:
                    balance = child_1.with_context({'date_from':self.start_date, 'date_to':self.end_date,'strict_range':True,'company_id':self.company_id.id}).balance
                    com_balance = child_1.with_context({'date_from':self.com_start_date, 'date_to':self.com_end_date,'strict_range':True,'company_id':self.company_id.id}).balance
                    if not child_1.user_type_id.type == 'view':
                        lst.append({
                            'x_name':'a'*count,
                            'name':child_1.code + ' '+ child_1.name,
                            'seq':count,
                            'is_bold':False,
                            'balance':balance,
                            'com_balance':com_balance,
                            })
                    else:
                        lst.append({
                            'x_name':'a'*count,
                            'name':child_1.code + ' '+ child_1.name,
                            'seq':count,
                            'is_bold':True,
                            'balance':balance,
                            'com_balance':com_balance,
                            })
                        count +=1
                        for child_2 in child_1.child_ids:
                            balance = child_2.with_context({'date_from':self.start_date, 'date_to':self.end_date,'strict_range':True,'company_id':self.company_id.id}).balance
                            com_balance = child_2.with_context({'date_from':self.com_start_date, 'date_to':self.com_end_date,'strict_range':True,'company_id':self.company_id.id}).balance
                            if not child_2.user_type_id.type == 'view':
                                lst.append({
                                    'x_name':'a'*(count+1),
                                    'name':child_2.code + ' '+ child_2.name,
                                    'seq':count,
                                    'is_bold':False,
                                    'balance':balance,
                                    'com_balance':com_balance,
                                    })
                            else:
                                lst.append({
                                    'x_name':'a'*(count+1),
                                    'name':child_2.code + ' '+ child_2.name,
                                    'seq':count,
                                    'is_bold':True,
                                    'balance':balance,
                                    'com_balance':com_balance,
                                    })
                                count +=1
                                for child_3 in child_2.child_ids:
                                    balance = child_3.with_context({'date_from':self.start_date, 'date_to':self.end_date,'strict_range':True,'company_id':self.company_id.id}).balance
                                    com_balance = child_3.with_context({'date_from':self.com_start_date, 'date_to':self.com_end_date,'strict_range':True,'company_id':self.company_id.id}).balance
                                    if not child_3.user_type_id.type == 'view':
                                        lst.append({
                                            'x_name':'a'*(count+2),
                                            'name':child_3.code + ' '+ child_3.name,
                                            'seq':count,
                                            'is_bold':False,
                                            'balance':balance,
                                            'com_balance':com_balance,
                                            })
                                    else:
                                        lst.append({
                                            'x_name':'a'*(count+2),
                                            'name':child_3.code + ' '+ child_3.name,
                                            'seq':count,
                                            'is_bold':True,
                                            'balance':balance,
                                            'com_balance':com_balance,
                                            })
                                        count +=1
                                        for child_4 in child_3.child_ids:
                                            balance = child_4.with_context({'date_from':self.start_date, 'date_to':self.end_date,'strict_range':True,'company_id':self.company_id.id}).balance
                                            com_balance = child_4.with_context({'date_from':self.com_start_date, 'date_to':self.com_end_date,'strict_range':True,'company_id':self.company_id.id}).balance
                                            if not child_4.user_type_id.type == 'view':
                                                lst.append({
                                                    'x_name':'a'*(count+3),
                                                    'name':child_4.code + ' '+ child_4.name,
                                                    'seq':count,
                                                    'is_bold':False,
                                                    'balance':balance,
                                                    'com_balance':com_balance,
                                                    })
                                            else:
                                                lst.append({
                                                    'x_name':'a'*(count+3),
                                                    'name':child_4.code + ' '+ child_4.name,
                                                    'seq':count,
                                                    'is_bold':True,
                                                    'balance':balance,
                                                    'com_balance':com_balance,
                                                    })
                                                count +=1
                                                for child_5 in child_4.child_ids:
                                                    balance = child_5.with_context({'date_from':self.start_date, 'date_to':self.end_date,'strict_range':True,'company_id':self.company_id.id}).balance
                                                    com_balance = child_5.with_context({'date_from':self.com_start_date, 'date_to':self.com_end_date,'strict_range':True,'company_id':self.company_id.id}).balance
                                                    if not child_5.user_type_id.type == 'view':
                                                        lst.append({
                                                            'x_name':'a'*(count+4),
                                                            'name':child_5.code + ' '+ child_5.name,
                                                            'seq':count,
                                                            'is_bold':False,
                                                            'balance':balance,
                                                            'com_balance':com_balance,
                                                            })
                                                    else:
                                                        lst.append({
                                                            'x_name':'a'*(count+4),
                                                            'name':child_5.code + ' '+ child_5.name,
                                                            'seq':count,
                                                            'is_bold':True,
                                                            'balance':balance,
                                                            'com_balance':com_balance,
                                                            })
        
                if lst:
                    final_lst.append(lst)  
                    count = 0  
        return final_lst
    
            

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:    
    
