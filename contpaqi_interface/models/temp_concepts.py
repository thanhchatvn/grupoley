# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools

class TemporalConcepts(models.TransientModel):
    _name = 'temporal.concepts'
    _description = 'Tabla de conceptos temporales'

    idperiodo = fields.Char(string='ID del periodo (CONTPAQi)',store=True)
    idempleado = fields.Char(string='ID del empleado (CONTPAQi)', store=True)
    idconcepto = fields.Char(string='ID del concepto (CONTPAQi)', store=True)
    importetotal = fields.Char(string='Importe Total (CONTPAQi)', store=True)
    importe1 = fields.Char(string='Importe 1 (CONTPAQi)', store=True)
    importe2 = fields.Char(string='Importe 2 (CONTPAQi)', store=True)
    importe3 = fields.Char(string='Importe 3 (CONTPAQi)', store=True)
    importe4 = fields.Char(string='Importe 4 (CONTPAQi)', store=True)
    tipoconcepto = fields.Char(string='Tipo de concepto (CONTPAQi)', store=True)
    descripcion_concepto = fields.Char(string='Descripcion del concepto (CONTPAQi)', store=True)
    naturaleza = fields.Char(string='Tipo de importe (CONTPAQi)', store=True)
    iddepartamento = fields.Char(string='Departamento (CONTPAQi)', store=True)
    company_id = fields.Many2one('res.company',string='Company',default=lambda self: self.env.company)

    @api.model
    def _get_concept_period(self,period):
        try:
            temporal_concepts_obj = self.env['temporal.concepts'].search([('company_id', '=', self.env.company.id)])
            temporal_concepts_obj.unlink()
            connection = self.env['contpaqi.interface'].server_connection()
            with connection.cursor() as cursor:
                cursor.execute("""
                    Select c.idperiodo,c.idempleado,c.idconcepto,c.importetotal,c.importe1,c.importe2,c.importe3,c.importe4,
                    m.tipoconcepto,m.descripcion as DescripcionConcepto,
                    Naturaleza=Case
                    When m.tipoconcepto='P' or m.tipoconcepto='O' then 'Cargo'
                    when m.tipoconcepto='D' then 'Abono'
                    end,n.iddepartamento
                    from nom10007 c(nolock)
                    inner join nom10004 m(nolock) on c.idconcepto=m.idconcepto  and m.especie=0
                    and m.Tipoconcepto in('D','P','O')
                    inner join nom10001 n(nolock) on c.idempleado=n.idempleado
                    where c.idperiodo=""" + str(period).strip() + """ and importetotal<>0""")
                batchs = cursor.fetchall()
                for batch in batchs:
                    data = {
                        'idperiodo': str(batch[0]).strip(),
                        'idempleado': str(batch[1]).strip(),
                        'idconcepto': str(batch[2]).strip(),
                        'importetotal': str(batch[3]).strip(),
                        'importe1': str(batch[4]).strip(),
                        'importe2': str(batch[5]).strip(),
                        'importe3': str(batch[6]).strip(),
                        'importe4': str(batch[7]).strip(),
                        'tipoconcepto': str(batch[8]).strip(),
                        'descripcion_concepto': str(batch[9]).strip(),
                        'naturaleza': str(batch[10]).strip(),
                        'iddepartamento': str(batch[11]).strip()
                    }
                    temporal_concepts_obj.create(data)
            return period

        except Exception as e:
            return period
            print('No es posible realizar la consulta get period concepts', e)


class TemporalConceptsFinal(models.Model):
    _name = 'temporal.concepts.final'
    _description = 'Tabla de conceptos temporales final'

    idperiodo = fields.Char(string='ID del periodo (CONTPAQi)',store=True)
    idempleado = fields.Char(string='ID del empleado (CONTPAQi)', store=True)
    idconcepto = fields.Char(string='ID del concepto (CONTPAQi)', store=True)
    importetotal = fields.Char(string='Importe Total (CONTPAQi)', store=True)
    importe1 = fields.Char(string='Importe 1 (CONTPAQi)', store=True)
    importe2 = fields.Char(string='Importe 2 (CONTPAQi)', store=True)
    importe3 = fields.Char(string='Importe 3 (CONTPAQi)', store=True)
    importe4 = fields.Char(string='Importe 4 (CONTPAQi)', store=True)
    tipoconcepto = fields.Char(string='Tipo de concepto (CONTPAQi)', store=True)
    descripcion_concepto = fields.Char(string='Descripcion del concepto (CONTPAQi)', store=True)
    naturaleza = fields.Char(string='Tipo de importe (CONTPAQi)', store=True)
    iddepartamento = fields.Char(string='Departamento (CONTPAQi)', store=True)
    tipo_concepto_de = fields.Char(string='Tipo de concepto departamento (CONTPAQi)',store=True)
    company_id = fields.Many2one('res.company',string='Company',default=lambda self: self.env.company)


    @api.model
    def _get_temporal_concept(self):
        try:
            temporal_concepts_final_obj = self.env['temporal.concepts.final'].search([('company_id', '=', self.env.company.id)])
            temporal_concepts_final_obj.unlink()
            tools.drop_view_if_exists(self.env.cr, 'temporal_concepts_final_view_tree')
            self.env.cr.execute("""
                                SELECT a.idperiodo,a.idempleado,a.idconcepto,a.importetotal,a.importe1,a.importe2,
                                       a.importe3,a.importe4,a.tipoconcepto,a.descripcion_concepto,a.naturaleza,
                                       a.iddepartamento
                                FROM temporal_concepts a
                                """)

            lista = []
            batchs = self.env.cr.fetchall()
            for batch in batchs:
                tipo = self.env['hr.salary.rule'].search(
                    ['&', '&','&',
                     ('x_concept_type', 'ilike', batch[8]),
                     ('x_contpaq_concept_id', '=', batch[2]),
                     ('x_contpaq_series', '=', self.env.company.x_payroll_series),
                     ('company_id','=',self.env.company.id)], limit=1)
                # print('Lista antes de modificar: ', batch)
                batch = list(batch)
                batch.append(tipo.x_type)
                batch = tuple(batch)
                lista.append(batch)
                # print('Lista despues de modificar: ',batch)

            for rec in lista:
                data = {
                    'idperiodo': str(rec[0]).strip(),
                    'idempleado': str(rec[1]).strip(),
                    'idconcepto': str(rec[2]).strip(),
                    'importetotal': str(rec[3]).strip(),
                    'importe1': str(rec[4]).strip(),
                    'importe2': str(rec[5]).strip(),
                    'importe3': str(rec[6]).strip(),
                    'importe4': str(rec[7]).strip(),
                    'tipoconcepto': str(rec[8]).strip(),
                    'descripcion_concepto': str(rec[9]).strip(),
                    'naturaleza': str(rec[10]).strip(),
                    'iddepartamento': str(rec[11]).strip(),
                    'tipo_concepto_de': str(rec[12]).strip()
                }
                temporal_concepts_final_obj.create(data)
            print('Satisfactorio')

        except Exception as e:
            print(e)