# -*- coding: utf-8 -*-
# from odoo import http


# class StockLot(http.Controller):
#     @http.route('/stock_lot/stock_lot/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_lot/stock_lot/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_lot.listing', {
#             'root': '/stock_lot/stock_lot',
#             'objects': http.request.env['stock_lot.stock_lot'].search([]),
#         })

#     @http.route('/stock_lot/stock_lot/objects/<model("stock_lot.stock_lot"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_lot.object', {
#             'object': obj
#         })
