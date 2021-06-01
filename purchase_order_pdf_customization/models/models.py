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
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def get_approval(self):
        id = self.id
        approval_line_entry = self.env['studio.approval.entry'].search([['res_id', '=', id], ['model', 'like', "purchase.order"]])
        return approval_line_entry.user_id.display_name


