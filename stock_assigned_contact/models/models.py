# -*- coding: utf-8 -*-
# author : Jesus Valdes
# Motrar en pantalla de transferencias internas el nombre del contacto
# 14-06-2021

from odoo import models, fields, api

class stock_contact(models.Model):
    _inherit = 'stock.picking'

    partner_id = fields.Many2one(
        'res.partner', 'Contact',
        check_company=True,
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]}, compute='_valores_contact')

    @api.depends('group_id.partner_id')
    def _valores_contact(self):
        for value in self:
            value.partner_id = value.group_id.partner_id.id



