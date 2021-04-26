# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    x_order_reference = fields.Char(string="Order Reference", store=True, compute="_get_order_reference",
                                   help='Specifies the purchase order reference (Buyer) that the invoice refers to.')
    x_order_reference_date = fields.Date(string='Order Date', store=True, compute="_get_order_date",
                                         help='Specifies the purchase order date (Buyer) that the invoice refers to.')
    x_additional_reference = fields.Char(string='Additional Reference', store=True,
                                         help='Aproval Number')
    x_delivery_reference = fields.Char(string='Delivery Reference', store=True,
                                       help='Folio number. Number issued by the buyer when he reviews the merchandise that is invoiced')
    x_delivery_reference_date = fields.Date(string='Delivery Date', store=True,
                                            help='Specifies the date the receipt folio number was assigned.')
    x_vendor_code = fields.Char(string="Vendor code", compute="_get_vendor_code")



    @api.depends('partner_id','invoice_line_ids.product_id')
    def _get_vendor_code(self):
        for rec in self:
            if rec.invoice_line_ids:
                for product in rec.invoice_line_ids:
                    if product.product_id:
                        for code in product.product_id.x_product_supplierinfo:
                            if code.vendor_code and code.partner_name == rec.partner_id:
                                vendor = code.vendor_code
                                rec.x_vendor_code = vendor
                                break
                            else:
                                continue
            else:
                rec.x_vendor_code = ""


    # @api.depends('ref')
    # def _get_order_reference(self):
    #     for rec in self:
    #         if rec.ref:
    #             rec['x_order_reference'] = rec.ref
    #         else:
    #             pass
    #
    # @api.depends('invoice_line_ids.sale_line_ids.order_id')
    # def _get_order_date(self):
    #     for rec in self:
    #         sale_model = 'sale_line_ids' in rec.invoice_line_ids._fields
    #         sale_id = rec.mapped('invoice_line_ids.sale_line_ids.order_id') if sale_model else False
    #         rec['x_order_reference_date'] = sale_id.x_studio_fecha_orden_de_compra
