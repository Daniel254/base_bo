# -*- coding: utf-8 -*-
# Copyright 2014-2015 Tecnativa S.L. - Jairo Llopis
# Copyright 2016 Tecnativa S.L. - Vicent Cubells
# Copyright 2017 Tecnativa S.L. - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Ciudad',
    "summary": "Ciudad ",
    'version': '10.0.1.0.0',
    'category': 'Customer Relationship Management',
    'author': 'Odoo Bolivia, '
              'Odoo Community Association (OCA)',
    "license": "AGPL-3",
    'website': 'http://www.odoo.org.bo',
    "application": False,
    'depends': [
        'sales_team',
    ],
    'data': [
        'views/res_partner_ciudad_view.xml',
        'views/res_partner_view.xml',
    ],
    "installable": True,
}
