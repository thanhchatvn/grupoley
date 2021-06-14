# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PosConfig(models.Model):
    _inherit = 'res.partner'

    ref = fields.Char(string='Referencia', default=True)
    category_id = fields.Many2one('res.partner.category',string='Referencia', default=True)