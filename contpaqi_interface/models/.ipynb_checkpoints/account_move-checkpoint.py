# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    payroll_policy = fields.Boolean(string='Poliza de nómina', default=False)