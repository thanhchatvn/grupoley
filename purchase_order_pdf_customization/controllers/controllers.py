# -*- coding: utf-8 -*-
# from odoo import http


# class SaleOrderPdfCustomization(http.Controller):
#     @http.route('/purchase_order_pdf_customization/purchase_order_pdf_customization/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchase_order_pdf_customization/purchase_order_pdf_customization/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchase_order_pdf_customization.listing', {
#             'root': '/purchase_order_pdf_customization/purchase_order_pdf_customization',
#             'objects': http.request.env['purchase_order_pdf_customization.purchase_order_pdf_customization'].search([]),
#         })

#     @http.route('/purchase_order_pdf_customization/purchase_order_pdf_customization/objects/<model("purchase_order_pdf_customization.purchase_order_pdf_customization"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchase_order_pdf_customization.object', {
#             'object': obj
#         })
