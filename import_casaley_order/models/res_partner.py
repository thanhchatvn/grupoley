# -*- coding: utf-8 -*-

from odoo import fields, models, api

class ImportChartAccount(models.Model):
    _inherit = "res.partner"

    x_route = fields.Many2one('route.pam',string='Ruta (ciudad)',store=True)
    x_zone = fields.Many2one('zone.pam',string='Territorio', store=True)