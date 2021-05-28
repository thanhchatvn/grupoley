# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools

class AccountingPolicy(models.Model):
    _name = 'contpaq.policy'
    _description = 'Poliza generada en CONTPAQi'

    naturaleza = fields.Char(string='Naturaleza', store=True)
    cuenta = fields.Char(string='Cuenta', store=True)
    importe = fields.Char(string='Importe', store=True)
    tipo = fields.Char(string='Tipo', store=True)
    id_empleado = fields.Char(string='Id Empleado', store=True)
    descripcion = fields.Char(string='Descripción', store=True)
    descripcion_concepto = fields.Char(string='Descripción Concepto', store=True)
    banco = fields.Char(string='Banco', store=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    analytic_account_id = fields.Many2one('account.analytic.account', 'Cuenta Analítica', company_dependent=True)
    account_debit = fields.Many2one('account.account', 'Cuenta Deudora', company_dependent=True,
                                    domain=[('deprecated', '=', False)])
    account_credit = fields.Many2one('account.account', 'Cuenta Acreedora', company_dependent=True,
                                     domain=[('deprecated', '=', False)])

    @api.model
    def _generate_policy(self):
        try:
            contpaqi_policy_obj = self.env['contpaq.policy'].search([('company_id', '=', self.env.company.id)])
            contpaqi_policy_obj.unlink()
            self.env.cr.execute("""
                SELECT t.naturaleza, l.x_contpaq_account, t.importetotal, t.tipo_concepto_de, 
                       t.idempleado, t.descripcion_concepto,t.descripcion_concepto,l.x_contpaq_bank, 
                       l.x_debit_id, l.x_credit_id, l.x_analytic_id
                FROM temporal_concepts_final t 
                inner join hr_salary_rule l on l.x_contpaq_concept_id=t.idconcepto and t.iddepartamento=l.x_contpaq_department_id and t.tipo_concepto_de=l.x_type and l.x_contpaq_series='""" +str(self.env.company.x_payroll_series)+ """'
                where t.tipo_concepto_de='D' and t.company_id='"""+str(self.env.company.id)+"""' and l.company_id='"""+str(self.env.company.id)+"""'
                """)
            batchs = self.env.cr.fetchall()
            print("\n\nCARGOS Y ABONOS TIPO D")
            for batch in batchs:
                data = {
                    'naturaleza': str(batch[0]).strip(),
                    'cuenta': str(batch[1]).strip(),
                    'importe': str(batch[2]).strip(),
                    'tipo': str(batch[3]).strip(),
                    'id_empleado': str(batch[4]).strip(),
                    'descripcion': str(batch[5]).strip(),
                    'descripcion_concepto': str(batch[6]).strip(),
                    'banco': str(batch[7]).strip(),
                    'account_debit' : batch[8],
                    'account_credit' : batch[9],
                    'analytic_account_id' : batch[10]
                }
                contpaqi_policy_obj.create(data)
                print(batch)

            print("\n\nCARGOS Y ABONOS TIPO E")

            self.env.cr.execute("""
                        SELECT t.naturaleza, l.x_contpaq_account, t.importetotal, t.tipo_concepto_de, 
                               t.idempleado, t.descripcion_concepto,t.descripcion_concepto,l.x_contpaq_bank,
                               l.x_debit_id, l.x_credit_id, l.x_analytic_id
                        FROM temporal_concepts_final t
                        inner join hr_salary_rule l on l.x_contpaq_concept_id=t.idconcepto and t.iddepartamento=l.x_contpaq_department_id and t.tipo_concepto_de=l.x_type and l.x_contpaq_series='""" + str(self.env.company.x_payroll_series).strip() + """'
                        where t.tipo_concepto_de='E' and t.company_id='"""+str(self.env.company.id)+"""' and l.company_id='"""+str(self.env.company.id)+"""'
                        """)
            batchs = self.env.cr.fetchall()
            for batch in batchs:
                data = {
                    'naturaleza': str(batch[0]).strip(),
                    'cuenta': str(batch[1]).strip(),
                    'importe': str(batch[2]).strip(),
                    'tipo': str(batch[3]).strip(),
                    'id_empleado': str(batch[4]).strip(),
                    'descripcion': str(batch[5]).strip(),
                    'descripcion_concepto': str(batch[6]).strip(),
                    'banco': str(batch[7]).strip(),
                    'account_debit': batch[8],
                    'account_credit': batch[9],
                    'analytic_account_id': batch[10]
                }
                contpaqi_policy_obj.create(data)
                print(batch)

            print("\n\nDE CARGOS A ABONOS TIPO D")
            self.env.cr.execute("""
                                SELECT
                                    Case
                                        When t.naturaleza='Cargo' then 'Abono'
                                        When t.naturaleza='Abono' then 'Cargo'
                                        Else ''
                                    End,

                                    l.x_contpaq_account,t.importetotal, t.tipo_concepto_de, t.idempleado, 
                                    t.descripcion_concepto,t.descripcion_concepto,l.x_contpaq_bank, 
                                    l.x_debit_id, l.x_credit_id, l.x_analytic_id
                                FROM temporal_concepts_final t
                                inner join hr_salary_rule l
                                    on l.x_contpaq_concept_id=t.idconcepto and t.iddepartamento=l.x_contpaq_department_id and t.tipo_concepto_de=l.x_type and l.x_contpaq_series='""" + self.env.company.x_payroll_series + """'
                                where t.tipo_concepto_de='D' and t.company_id='"""+str(self.env.company.id)+"""' and l.company_id='"""+str(self.env.company.id)+"""'
                                """)
            batchs = self.env.cr.fetchall()
            for batch in batchs:
                data = {
                    'naturaleza': str(batch[0]).strip(),
                    'cuenta': str(batch[1]).strip(),
                    'importe': str(batch[2]).strip(),
                    'tipo': str(batch[3]).strip(),
                    'id_empleado': str(batch[4]).strip(),
                    'descripcion': str(batch[5]).strip(),
                    'descripcion_concepto': str(batch[6]).strip(),
                    'banco': str(batch[7]).strip(),
                    'account_debit': batch[8],
                    'account_credit': batch[9],
                    'analytic_account_id': batch[10]
                }
                contpaqi_policy_obj.create(data)
                print(batch)

            print("\n\nDE CARGOS A ABONOS TIPO E")
            self.env.cr.execute("""
                                SELECT
                                    Case
                                        When t.naturaleza='Cargo' then 'Abono'
                                        When t.naturaleza='Abono' then 'Cargo'
                                        Else ''
                                    End,

                                    l.x_contpaq_account,t.importetotal, t.tipo_concepto_de, t.idempleado, 
                                    t.descripcion_concepto,t.descripcion_concepto,l.x_contpaq_bank, 
                                    l.x_debit_id, l.x_credit_id, l.x_analytic_id
                                FROM temporal_concepts_final t
                                inner join hr_salary_rule l
                                    on l.x_contpaq_concept_id=t.idconcepto and t.iddepartamento=l.x_contpaq_department_id and t.tipo_concepto_de=l.x_type and l.x_contpaq_series='""" + self.env.company.x_payroll_series + """'
                                where t.tipo_concepto_de='E' and t.company_id='"""+str(self.env.company.id)+"""' and l.company_id='"""+str(self.env.company.id)+"""'
                                """)
            batchs = self.env.cr.fetchall()
            for batch in batchs:
                data = {
                    'naturaleza': str(batch[0]).strip(),
                    'cuenta': str(batch[1]).strip(),
                    'importe': str(batch[2]).strip(),
                    'tipo': str(batch[3]).strip(),
                    'id_empleado': str(batch[4]).strip(),
                    'descripcion': str(batch[5]).strip(),
                    'descripcion_concepto': str(batch[6]).strip(),
                    'banco': str(batch[7]).strip(),
                    'account_debit': batch[8],
                    'account_credit': batch[9],
                    'analytic_account_id': batch[10]
                }
                contpaqi_policy_obj.create(data)
                print(batch)
        except Exception as e:
            print(e)

