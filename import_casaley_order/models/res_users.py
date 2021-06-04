# -*- coding: utf-8 -*-

from odoo import fields, models, api

class ResUsers(models.Model):
    _name = 'res.users'
    _inherit = 'res.users'

    x_comercial = fields.Boolean(string='Es comercial',default=False)