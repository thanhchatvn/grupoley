# -*- coding: utf-8 -*-
from odoo import api, fields, models

class ZonePam(models.Model):
    _name = 'zone.pam'
    _description = 'Territorios en el PAM'

    name = fields.Char(string='Territorio', store=True)
    code = fields.Char(string='Código', store=True)