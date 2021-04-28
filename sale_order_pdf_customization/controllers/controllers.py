# -*- coding: utf-8 -*-
# from odoo import http


# class SaleOrderPdfCustomization(http.Controller):
#     @http.route('/sale_order_pdf_customization/sale_order_pdf_customization/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_order_pdf_customization/sale_order_pdf_customization/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_order_pdf_customization.listing', {
#             'root': '/sale_order_pdf_customization/sale_order_pdf_customization',
#             'objects': http.request.env['sale_order_pdf_customization.sale_order_pdf_customization'].search([]),
#         })

#     @http.route('/sale_order_pdf_customization/sale_order_pdf_customization/objects/<model("sale_order_pdf_customization.sale_order_pdf_customization"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_order_pdf_customization.object', {
#             'object': obj
#         })
