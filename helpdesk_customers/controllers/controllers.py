# -*- coding: utf-8 -*-
# from odoo import http


# class HelpdeskCustomers(http.Controller):
#     @http.route('/helpdesk_customers/helpdesk_customers/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/helpdesk_customers/helpdesk_customers/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('helpdesk_customers.listing', {
#             'root': '/helpdesk_customers/helpdesk_customers',
#             'objects': http.request.env['helpdesk_customers.helpdesk_customers'].search([]),
#         })

#     @http.route('/helpdesk_customers/helpdesk_customers/objects/<model("helpdesk_customers.helpdesk_customers"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('helpdesk_customers.object', {
#             'object': obj
#         })
