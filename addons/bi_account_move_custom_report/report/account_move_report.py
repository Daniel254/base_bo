# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import time
from datetime import date, datetime
from odoo.exceptions import Warning
from odoo import models, fields, exceptions, api, _
from odoo.exceptions import UserError, ValidationError

class ReportWizard(models.TransientModel):
    _name = "account.move.report.wizard"

    x_nro = fields.Char('x_nro', required = True)
    
    @api.multi
    def submit(self):
        temp = [] 
        list_of_data = []
        line_dic = {}
        dic_of_date = {}
        dic_of_date1 = {}
        list_of_date = []
        list_of_label = []
        account_move_ids = self.env['account.move'].search([('x_nro','=',self.x_nro)])
        create_date = account_move_ids[0].create_date
        date_format = datetime.strptime(create_date, '%Y-%m-%d %H:%M:%S')
        current_date = date_format.strftime("%Y-%m-%d")
        res_user_obj = self.env['res.users'].browse(account_move_ids[0].create_uid.id)
        res_user_name = res_user_obj.name
        
        if not account_move_ids:
            raise UserError(_('There Is No Any Account Move Details.'))
        else:
            '''for move in account_move_ids:
                for line in move.line_ids:
                    if line.account_id not in line_dic:
                        line_dic.update({
                                            'account_id' : line.account_id,
                                            'partner_id' : line.partner_id,
                                           })'''
            for move in account_move_ids:
                for line in move.line_ids:
                    list_of_date.append(line.date_maturity)
                    list_of_label.append(line.name)
                    #dic_of_date.update({'partner_id':line.partner_id.id,'account_id':line.account_id.id,'date_maturity':line.date_maturity})
                    '''
                    if (line.partner_id.id == dic_of_date.get('partner_id') and line.account_id.id == dic_of_date.get('account_id')):
                        dic_of_date.update({'date_maturiry':line.date_maturity})
                        list_of_date.append(dic_of_date)
                    else:
                        dic_of_date.update({'partner_id':line.partner_id.id,'account_id':line.account_id.id,'date_maturity':line.date_maturity})
                        dic_of_date1.update({'partner_id':line.partner_id.id,'account_id':line.account_id.id,'date_maturity':line.date_maturity})
                        list_of_date.append(dic_of_date1)'''
                        

            self.env.cr.execute('select date_maturity,account_id,partner_id from account_move_line where move_id in (select id from account_move where x_nro=%s) group by account_id,partner_id,date_maturity order by account_id ASC', ([self.x_nro]))
            summary_data1 = self.env.cr.dictfetchall()
            
                                                          
            self.env.cr.execute('select sum(credit) as Credit,sum(debit) as Debit,account_id,partner_id from account_move_line where move_id in (select id from account_move where x_nro=%s) group by account_id,partner_id order by account_id ASC', ([self.x_nro]))
            summary_data = self.env.cr.dictfetchall()
            
            account_name = ''
            
            for val  in summary_data:
                account_obj = self.env['account.account'].browse(val.get('account_id'))
                account_name = account_obj.code + ' ' + account_obj.name
                partner_obj = self.env['res.partner'].browse(val.get('partner_id')).name
                val.update({'account_id':account_name,'partner_id':partner_obj,'date_maturity':list_of_date[0],'name':list_of_label[0]})
                list_of_data.append(val)
                del list_of_date[0]
                del list_of_label[0]
            
            #list_of_data.append(val)
            
        data = list_of_data
        datas = {
            'ids': self._ids,
            'model': 'account.move',
            'form': data,
            'x_nro':self.x_nro,
            'date' : account_move_ids[0].date,
            'journal_id' : account_move_ids[0].journal_id.name,
            'create_date':current_date,
            'create_uid' : res_user_name,
            'tipo_id' : account_move_ids[0].tipo_id.name,
            #'list_of_data' : list_of_data,
        }
        return self.env['report'].get_action(self, 'bi_account_move_custom_report.account_move_template', data=datas)
        
class account_move_template(models.AbstractModel):
    _name = 'report.bi_account_move_custom_report.account_move_template'

    @api.multi
    def render_html(self,docids, data=None):
        list_of_data = []
        report_obj = self.env['report']
        #record_ids = self.env[data['model']].browse(data['form'])
        report = report_obj._get_report_from_name('bi_account_move_custom_report.account_move_template')
        docargs = {
                   'doc_ids': docids,
                   'doc_model': 'account.move',
                   'docs': data['form'],
                   'data' : data,
                   'date' : data['date'],
                   'journal_id' : data['journal_id'],
                   'create_date':data['create_date'],
                   'create_uid' : data['create_uid'],
                   'tipo_id' : data['tipo_id'],
                   #'list_of_data' : list_of_data,
                   }
        return report_obj.render('bi_account_move_custom_report.account_move_template', docargs)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

