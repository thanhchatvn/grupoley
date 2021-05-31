# -*- coding: utf-8 -*-
# from odoo import http


# class CustomPromotions(http.Controller):
#     @http.route('/custom_promotions/custom_promotions/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_promotions/custom_promotions/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_promotions.listing', {
#             'root': '/custom_promotions/custom_promotions',
#             'objects': http.request.env['custom_promotions.custom_promotions'].search([]),
#         })

#     @http.route('/custom_promotions/custom_promotions/objects/<model("custom_promotions.custom_promotions"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_promotions.object', {
#             'object': obj
#         })
