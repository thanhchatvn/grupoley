# # -*- coding: utf-8 -*-
from odoo import models, fields, api

class HelpdeskTicket(models.Model):
    # Heredamos el módelo que deseamos modificar 
    _inherit = 'helpdesk.ticket'    
    
    # Creamos el campo el cual estara relacionado para obtener los datos deseados
    x_parent_id = fields.Many2one(string='Compañía Relacionada', related='partner_id.commercial_partner_id',
                                  readonly=True, store=True)
    