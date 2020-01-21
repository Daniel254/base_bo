# -*- coding: utf-8 -*-

from odoo import models


class AccMoveReport2(models.Model):
    _inherit = 'account.move'

    def print_journal_entry2(self):
        return self.env['report'].get_action(self, 'check_reports_journal_entry.tmpte_journal_entry2')
