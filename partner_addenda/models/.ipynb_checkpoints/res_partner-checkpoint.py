# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    x_gln = fields.Char(string='GLN', store=True, help='Global Location Number')