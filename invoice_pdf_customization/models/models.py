# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class invoice_pdf_customization(models.Model):
#     _name = 'invoice_pdf_customization.invoice_pdf_customization'
#     _description = 'invoice_pdf_customization.invoice_pdf_customization'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
class AccountInvoice(models.Model):
    _inherit = 'account.move'

    def calculate_cfdi_values_pdf(self):
        self.ensure_one()
        invoice = self.sudo()
        cfdi_values = {}
        for line in invoice.invoice_line_ids:
            cfdi_values[line.id] = {}
            cfdi_values[line.id]['wo_discount'] = line.price_unit * (1 - (line.discount / 100.0))
            cfdi_values[line.id]['total_wo_discount'] = invoice.currency_id.round(line.price_unit * line.quantity)
            cfdi_values[line.id]['discount_amount'] = invoice.currency_id.round(
                cfdi_values[line.id]['total_wo_discount'] - line.price_subtotal)
            cfdi_values[line.id]['price_subtotal_unit'] = invoice.currency_id.round(cfdi_values[line.id]['total_wo_discount'] / line.quantity)
        return cfdi_values

