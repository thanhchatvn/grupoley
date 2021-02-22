# -*- coding: utf-8 -*-
# from odoo import http


# class StockDeliveryReport(http.Controller):
#     @http.route('/stock_delivery_report/stock_delivery_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_delivery_report/stock_delivery_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_delivery_report.listing', {
#             'root': '/stock_delivery_report/stock_delivery_report',
#             'objects': http.request.env['stock_delivery_report.stock_delivery_report'].search([]),
#         })

#     @http.route('/stock_delivery_report/stock_delivery_report/objects/<model("stock_delivery_report.stock_delivery_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_delivery_report.object', {
#             'object': obj
#         })
