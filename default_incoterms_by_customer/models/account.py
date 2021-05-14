# -*- coding: utf-8 -*-

from odoo import models, fields, api

'''
    /*************************************************************************
    * Description
    * Se modifico el modelo de account.move para calcular el de incoterms dependiendo del colocado en
      el cliente.
    * 1.0
    * Author:
    * Erick Enrique Abrego Gonzalez
    * Date:
    * 14/05/2021
    *************************************************************************/
'''

class account(models.Model):
    _inherit = 'account.move'

    invoice_incoterm_id = fields.Many2one('account.incoterms', string='Incoterm',
                                          store=True, readonly=False,
                                          compute='_get_incoterm_from_customer',
                                          help='International Commercial Terms are a series of predefined commercial terms used in international transactions.')

    @api.depends('partner_id')
    def _get_incoterm_from_customer(self):
        for rec in self:
            if rec.partner_id.x_incoterms:
                rec.invoice_incoterm_id = rec.partner_id.x_incoterms
            else:
                rec.invoice_incoterm_id = rec.env.company.incoterm_id