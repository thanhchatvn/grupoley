# -*- coding: utf-8 -*-
# from odoo import http


# class PurchaseOrderReport(http.Controller):
#     @http.route('/purchase_order_report/purchase_order_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchase_order_report/purchase_order_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchase_order_report.listing', {
#             'root': '/purchase_order_report/purchase_order_report',
#             'objects': http.request.env['purchase_order_report.purchase_order_report'].search([]),
#         })

#     @http.route('/purchase_order_report/purchase_order_report/objects/<model("purchase_order_report.purchase_order_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchase_order_report.object', {
#             'object': obj
#         })
