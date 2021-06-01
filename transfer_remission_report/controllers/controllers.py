# -*- coding: utf-8 -*-
# from odoo import http


# class TransferRemissionReport(http.Controller):
#     @http.route('/transfer_remission_report/transfer_remission_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/transfer_remission_report/transfer_remission_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('transfer_remission_report.listing', {
#             'root': '/transfer_remission_report/transfer_remission_report',
#             'objects': http.request.env['transfer_remission_report.transfer_remission_report'].search([]),
#         })

#     @http.route('/transfer_remission_report/transfer_remission_report/objects/<model("transfer_remission_report.transfer_remission_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('transfer_remission_report.object', {
#             'object': obj
#         })
