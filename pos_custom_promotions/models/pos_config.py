# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    general_promotions = fields.Boolean(string='Promocion', default=True)