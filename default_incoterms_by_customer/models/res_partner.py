# -*- coding: utf-8 -*-

from odoo import models, fields, api

'''
    /*************************************************************************
    * Description
    * Se modifico el modelo de res.partner para agregar un campo relacionado a incoterms para
      los tratos de comercio internacional dependiendo del cliente en la facturacion
    * 1.0
    * Author:
    * Erick Enrique Abrego Gonzalez
    * Date:
    * 14/05/2021
    *************************************************************************/
'''

class default_incoterms_by_customer(models.Model):
    _inherit = 'res.partner'

    x_incoterms = fields.Many2one('account.incoterms',string='Incoterms',store=True)


