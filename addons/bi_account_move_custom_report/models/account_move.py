# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import time
from datetime import date, datetime
from odoo.exceptions import Warning
from odoo import models, fields, exceptions, api, _

class AccountMove(models.Model):
	_inherit = 'account.move'

	nro_number = fields.Char(string='Auxiliar',readonly=True)
	tipo_id = fields.Many2one('tipo.report',string='Tipo Comprobante')
	x_nro = fields.Char(string='Nro Comprobante')

	@api.model
	def create(self, vals):
		result = super(AccountMove, self).create(vals)
		invoice = self._context.get('invoice', False)
		tipo_income_template_id = self.env['ir.model.data'].xmlid_to_object('bi_account_move_custom_report.tipo_report_1')
		tipo_expense_template_id = self.env['ir.model.data'].xmlid_to_object('bi_account_move_custom_report.tipo_report_2')
		tipo_internal_template_id = self.env['ir.model.data'].xmlid_to_object('bi_account_move_custom_report.tipo_report_3')
		if self._context.get('type') == 'out_invoice'  or vals.get('tipo_id') == 1:
			result['tipo_id'] = tipo_income_template_id.id
			result['nro_number'] = self.env['ir.sequence'].next_by_code('income.tipo.report') or 'INCOME'
		elif self._context.get('type') == 'in_invoice'  or vals.get('tipo_id') == 2:
			result['tipo_id'] = tipo_expense_template_id.id
			result['nro_number'] = self.env['ir.sequence'].next_by_code('expense.tipo.report') or 'Expense'
		elif vals.get('tipo_id') == 3:
			result['tipo_id'] = tipo_internal_template_id.id
			result['nro_number'] = self.env['ir.sequence'].next_by_code('transfer.tipo.report') or 'Internal'
		else:
			result['tipo_id'] = tipo_internal_template_id.id
			result['nro_number'] = self.env['ir.sequence'].next_by_code('transfer.tipo.report') or 'Internal'
		return result
		

class TipoReport(models.Model):
	_name = 'tipo.report'

	name = fields.Char(string="Nombre")
	code = fields.Char(string="Codigo")
