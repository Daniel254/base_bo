# -*- coding: utf-8 -*-
# © 2018 Odoo Bolivia - Mauricio Carreño S.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    ciudad_id = fields.Many2one(
        "res.partner.ciudad",
        "Ciudad",
        oldname="ciudad")


class ResPartnerCiudad(models.Model):
    _name = 'res.partner.ciudad'
    _order = "parent_left"
    _parent_order = "name"
    _parent_store = True
    _description = "Ciudad"

    name = fields.Char(required=True, translate=True)
    codigo = fields.Char(required=True)
    parent_id = fields.Many2one(
        "res.partner.ciudad",
        "País",
        ondelete='restrict')
    parent_left = fields.Integer(index=True)
    parent_right = fields.Integer(index=True)

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(
                _('Error! You cannot create recursive ciudades.'))
