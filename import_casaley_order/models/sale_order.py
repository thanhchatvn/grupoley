#-*- coding: utf-8 -*-

'''
    /*************************************************************************
    * Description
    * Se añadieron dos campos necesarios para el llenado automático cuando se realicen los
      pedidos por medio de importannción.
    * 1.0
    * Author:
    * Erick Enrique Abrego Gonzalez
    * Date:
    * 16/04/2021
    *************************************************************************/
'''

from odoo import fields, models, api

class ImportChartAccount(models.Model):
    _inherit = "sale.order"

    x_order_reference = fields.Char(string="Folio de orden de compra")
    x_order_reference_date = fields.Char(string="Fecha de orden de compra")

    def _prepare_invoice(self):
        res = super(ImportChartAccount, self)._prepare_invoice()
        if self.x_order_reference and self.x_order_reference_date:
            res['x_order_reference'] = self.x_order_reference
            res['x_order_reference_date'] = self.x_order_reference_date
        return res

class SaleAdvanced(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _prepare_invoice_values(self, order, name, amount, so_line):
        res = super(SaleAdvanced, self)._prepare_invoice_values(order,name,amount,so_line)
        if order.x_order_reference and order.x_order_reference_date:
            res['x_order_reference'] = order.x_order_reference
            res['x_order_reference_date'] = order.x_order_reference_date
        return res
