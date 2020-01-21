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

class dev_general_ledger_report(models.TransientModel):
    _name = "dev.general.ledger.report"
    
    
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
    filter_account = fields.Boolean('Filter Accounts')
    filter_journal = fields.Boolean('Filter Journals')
    filter_partner = fields.Boolean('Filter Partners')
    account_ids = fields.Many2many('account.account', string='Accounts')
    journal_ids = fields.Many2many('account.journal', string='Journals')
    partner_ids = fields.Many2many('res.partner', string='Partners')
    group_by = fields.Selection([('date','Date'),('document','Document')], string='Group By', default='date')
    company_id = fields.Many2one('res.company', default=lambda self:self.env.user.company_id)
    target_moves = fields.Selection([('all','All Entries'),('posted','All Posted Entries')], default='posted', string='Target Moves')
    
    
    @api.multi
    def print_general_entry_report(self):
        return self.env['report'].get_action(self,'dev_account_report.dev_general_ledger_report')
        
    @api.multi
    def get_move_lines(self):
        state = ('posted',)
        if self.target_moves == 'all':
            state = ('draft','posted')
        params_lst = [self.start_date,self.end_date, self.company_id.id, state]
        account_filter = ''
        if self.filter_account:
            account_filter = ' AND aml.account_id in %s'
            params_lst.append(tuple(self.account_ids.ids))
        
        journal_filter = ''
        if self.filter_journal:
            journal_filter = ' AND aml.journal_id in %s'
            params_lst.append(tuple(self.journal_ids.ids))
            
        partner_filter = ''
        if self.filter_partner:
            partner_filter = ' AND aml.partner_id in %s'
            params_lst.append(tuple(self.partner_ids.ids))
            
        sql_query = """select aml.date, am.name as journal_entry, aml.name, aml.debit, aml.credit, aml.balance from account_move_line aml LEFT JOIN account_move am on aml.move_id = am.id where aml.date BETWEEN %s AND %s AND aml.company_id = %s AND am.state in %s"""+ account_filter +journal_filter + partner_filter
        
        params = tuple(params_lst)
        self.env.cr.execute(sql_query, params)
        lines = self.env.cr.dictfetchall()
        if lines:
            for line in lines:
                if not line.get('date'):
                    line['date'] = 'UNKNOWN'
                if not line.get('journal_entry'):
                    line['journal_entry'] = 'UNKNOWN'
                    
                    
            if self.group_by == 'date':
                n_lines=sorted(lines,key=itemgetter('date'))
                groups = itertools.groupby(n_lines, key=operator.itemgetter('date'))
                lines = [{'group_by':k,'values':[x for x in v]} for k, v in groups] 
            else:
                n_lines=sorted(lines,key=itemgetter('journal_entry'))
                groups = itertools.groupby(n_lines, key=operator.itemgetter('journal_entry'))
                lines = [{'group_by':k,'values':[x for x in v]} for k, v in groups]
        
        return lines
    
            

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:    
    
