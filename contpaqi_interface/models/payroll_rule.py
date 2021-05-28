# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PayrollRule(models.Model):
    _inherit = 'hr.salary.rule'

    x_concept_type = fields.Char(string='Tipo de concepto',store=True)
    x_type = fields.Char(string='Tipo',store=True)
    x_contpaq_concept_id = fields.Char(string='ID Concepto (CONTPAQ)',store=True)
    x_contpaq_department_id = fields.Char(string='ID Departamento (CONTPAQ)', store=True)
    x_contpaq_account = fields.Char(string='Cuenta gravada (CONTPAQ)', store=True)
    x_contpaq_exempt_account = fields.Char(string='Cuenta excenta',store=True)
    x_conterpart_account = fields.Char(string='Cuenta Contra Partida',store=True)
    x_contpaq_series = fields.Char(string='Serie (CONTPAQ)',store=True)
    x_contpaq_bank = fields.Char(string='Cuenta de banco (CONTPAQi)',store=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    x_analytic_id = fields.Integer(string='Cuenta analítica',related='analytic_account_id.id', store=True)
    x_debit_id = fields.Integer(string='Cuenta deudora',related='account_debit.id', store=True)
    x_credit_id = fields.Integer(string='Cuenta acredora',related='account_credit.id', store=True)
