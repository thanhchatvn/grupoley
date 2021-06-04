# -*- coding: utf-8 -*-

from odoo import fields, models, api

class ImportChartAccount(models.Model):
    _inherit = "res.partner"

    x_zone = fields.Many2one('zone.pam',string='Territorio', store=True)