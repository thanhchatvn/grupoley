# -*- coding: utf-8 -*-
# from odoo import http


# class DiscountInMxInvoicePdf(http.Controller):
#     @http.route('/discount_in_mx_invoice_pdf/discount_in_mx_invoice_pdf/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/discount_in_mx_invoice_pdf/discount_in_mx_invoice_pdf/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('discount_in_mx_invoice_pdf.listing', {
#             'root': '/discount_in_mx_invoice_pdf/discount_in_mx_invoice_pdf',
#             'objects': http.request.env['discount_in_mx_invoice_pdf.discount_in_mx_invoice_pdf'].search([]),
#         })

#     @http.route('/discount_in_mx_invoice_pdf/discount_in_mx_invoice_pdf/objects/<model("discount_in_mx_invoice_pdf.discount_in_mx_invoice_pdf"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('discount_in_mx_invoice_pdf.object', {
#             'object': obj
#         })
