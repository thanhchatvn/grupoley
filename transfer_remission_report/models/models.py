# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class transfer_remission_report(models.Model):
#     _name = 'transfer_remission_report.transfer_remission_report'
#     _description = 'transfer_remission_report.transfer_remission_report'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class TransferRemision(models.Model):
    _inherit = "stock.picking"

    def calculate_remission_details(self):
        self.ensure_one()
        picking = self.sudo()
        cfdi_values = {}
        for line in picking.move_ids_without_package:
            sale_line = line.sale_line_id
            if not line.product_id or not line.quantity_done:
                continue
            cfdi_values[sale_line.id] = {}
            cfdi_values[sale_line.id]['wo_discount'] = sale_line.price_unit * (1 - (sale_line.discount / 100.0))
            cfdi_values[sale_line.id]['total_wo_discount'] = picking.sale_id.currency_id.round(sale_line.price_unit * line.quantity_done)
            cfdi_values[sale_line.id]['discount_amount'] = picking.sale_id.currency_id.round(
                cfdi_values[sale_line.id]['total_wo_discount'] - sale_line.price_subtotal)
            cfdi_values[sale_line.id]['price_subtotal_unit'] = picking.sale_id.currency_id.round(cfdi_values[sale_line.id]['total_wo_discount'] / line.quantity_done)
            cfdi_values[sale_line.id]['discount_amount_price_list'] = (sale_line.product_id.list_price if sale_line.product_id.list_price > 1 else sale_line.price_unit - sale_line.price_unit) * line.quantity_done

            if sale_line.price_unit == 0.010000:
                cfdi_values[sale_line.id]['discount_amount_price_list'] = 0.0
            cfdi_values[sale_line.id]['line_original'] = sale_line
            cfdi_values[sale_line.id]['line_qty'] = line.quantity_done
        return cfdi_values