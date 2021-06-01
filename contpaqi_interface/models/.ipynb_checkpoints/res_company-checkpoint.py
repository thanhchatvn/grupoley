# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResCompany(models.Model):
    _inherit = 'res.company'

    x_company_payroll_db = fields.Char(string='Base de datos (Nomina)',store=True)
    x_payroll_series = fields.Char(string='Serie de nomina', store=True)
