# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class discount_in_mx_invoice_pdf(models.Model):
#     _name = 'discount_in_mx_invoice_pdf.discount_in_mx_invoice_pdf'
#     _description = 'discount_in_mx_invoice_pdf.discount_in_mx_invoice_pdf'

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

            cfdi_values[line.id]['discount_rate'] = line.sale_line_ids.discount_rate and line.sale_line_ids.discount_original or  line.sale_line_ids.discount and line.sale_line_ids.discount or 0.0
            cfdi_values[line.id]['discount_promotion'] = (0.01) if line.sale_line_ids.is_reward_line else 0
            cfdi_values[line.id]['discount_amount_price_list'] = (line.quantity * line.price_unit) * (cfdi_values[line.id]['discount_rate']/100.0)
        return cfdi_values

