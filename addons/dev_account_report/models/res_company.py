# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class res_company(models.Model):
    _inherit = 'res.company'


    profit_loss_account_ids  = fields.Many2many('account.account','pro_loss_company_rel','pro_loss_id','company_id', string='Profit Loss Accounts')
    balance_sheet_account_ids  = fields.Many2many('account.account','balance_sheet_company_rel','balance_sheet_id','company_id', string='Balance Sheet Accounts')
    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
