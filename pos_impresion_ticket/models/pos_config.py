# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    imprimir_ticket = fields.Boolean(string='Impresión del ticket', default=True)