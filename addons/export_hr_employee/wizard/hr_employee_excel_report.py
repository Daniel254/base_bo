# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
import xlwt
import datetime
import unicodedata
import base64
import StringIO
import csv, cStringIO
from datetime import datetime

class HrEmployeeExcelReport(models.TransientModel):
    
    _name = 'hr.employee.excel.report'
    _description = 'HR Employee Excel Report'

    company_id = fields.Many2one('res.company','Company',required=True)
    
    @api.multi
    def genarate_excel_report(self):
        custom_value = {}                 
        employee_obj = self.env['hr.employee']
        employee_sea = employee_obj.search([('company_id','=',self.company_id.id)])
        workbook = xlwt.Workbook()
        
        
        #Style for Excel
        style0 = xlwt.easyxf('font: name Times New Roman bold on;align: horiz left;', num_format_str='#,##0.00')
        style1 = xlwt.easyxf('font: name Times New Roman bold on; pattern: pattern solid, fore_colour black;align: horiz center;', num_format_str='#,##0.00')
        style2 = xlwt.easyxf('font:height 400,bold True; pattern: pattern solid, fore_colour black;', num_format_str='#,##0.00')         
        style3 = xlwt.easyxf('font:bold True;', num_format_str='#,##0.00')
        style4 = xlwt.easyxf('font:bold True;  borders:top double;align: horiz right;', num_format_str='#,##0.00')
        style5 = xlwt.easyxf('font: name Times New Roman bold on;align: horiz center;', num_format_str='#,##0')
        style6 = xlwt.easyxf('font: name Times New Roman bold on;', num_format_str='#,##0.00')
        style7 = xlwt.easyxf('font:bold True;  borders:top double;', num_format_str='#,##0.00')

        #Excel Heading Manipulation        
        sheet = workbook.add_sheet("Employee List")
        sheet.write(0,0,'Name', style0)
        sheet.write(0,1,'Mobile', style0)
        sheet.write(0,2,'Email', style0)
        sheet.write(0,3,'Phone', style0)
        sheet.write(0,4,'Title', style0)

        row = 1
        for rec in employee_sea:                
            sheet.write(row, 0, rec.name, style0)
            sheet.write(row, 1, rec.mobile_phone, style0)
            sheet.write(row, 2, rec.work_email, style0)
            sheet.write(row, 3, rec.work_phone, style0)
            sheet.write(row, 4, rec.job_id.name, style0)
            row +=1

        workbook.save('/tmp/employee_list.xls')
        result_file = open('/tmp/employee_list.xls','rb').read()
        attach_id = self.env['wizard.excel.report'].create({
                                        'name':'Employee List.xls',
                                        'report':base64.encodestring(result_file)
                    })
        return {
            'name': _('Notification'),
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'wizard.excel.report',
            'res_id':attach_id.id,
            'data': None,
            'type': 'ir.actions.act_window',
            'target':'new'
        }
                
class WizardExcelReport(models.TransientModel):
    _name = "wizard.excel.report"
    
    report = fields.Binary('Prepared file',filters='.xls', readonly=True)
    name = fields.Char('File Name', size=32)