# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Asset(models.Model):
    _inherit = 'account.asset'

    x_hr_department = fields.Many2one('hr.department', string="Departamento", store=True)
    x_inpc = fields.Float(string="INPC", store=True, digits=(16, 3))




