# -*- coding: utf-8 -*-
# from odoo import http


# class InvoicePdfCustomization(http.Controller):
#     @http.route('/invoice_pdf_customization/invoice_pdf_customization/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/invoice_pdf_customization/invoice_pdf_customization/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('invoice_pdf_customization.listing', {
#             'root': '/invoice_pdf_customization/invoice_pdf_customization',
#             'objects': http.request.env['invoice_pdf_customization.invoice_pdf_customization'].search([]),
#         })

#     @http.route('/invoice_pdf_customization/invoice_pdf_customization/objects/<model("invoice_pdf_customization.invoice_pdf_customization"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('invoice_pdf_customization.object', {
#             'object': obj
#         })
