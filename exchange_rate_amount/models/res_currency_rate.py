# -*- coding: utf-8 -*-
'''
    /*************************************************************************
    * Description
    * Se modifico el módelo de 'res.currency.rate' para añadir un campo nuevo que nos permita calcular
      el monto de la tasa de cambio y tener una mejor visibilidad de la cantidad.
    * 1.0
    * Author:
    * Erick Enrique Abrego Gonzalez
    * Date:
    * 21/04/2021
    *************************************************************************/
'''

from odoo import models, fields, api

class Currency(models.Model):
    _inherit = 'res.currency.rate'

    x_exchange_rate = fields.Float(string='Tasa de cambio', compute='_get_rate_change', digits=(12,4))

    @api.depends('rate')
    def _get_rate_change(self):
        for rec in self:
            rec.x_exchange_rate = 1 / rec.rate