# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _name = 'contpaq.payroll.line'
    _description = 'Poliza generada en CONTPAQi'

    account = fields.Char(string='Cuenta',store=True)
    description = fields.Char(string='Descripción',store=True)
    debit = fields.Char(string='Cargo',store=True)
    credit = fields.Char(string='Abono',store=True)
    payroll_id = fields.Many2one('contpaqi.interface')
    analytic_account_id = fields.Many2one('account.analytic.account', 'Cuenta Analítica', company_dependent=True)
    account_debit = fields.Many2one('account.account', 'Cuenta deudora', company_dependent=True,
                                    domain=[('deprecated', '=', False)])
    account_credit = fields.Many2one('account.account', 'Cuenta acreedora', company_dependent=True,
                                     domain=[('deprecated', '=', False)])


