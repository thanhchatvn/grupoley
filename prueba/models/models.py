# -*- coding: utf-8 -*-

from odoo import models, fields, api


class prueba(models.Model):
    _name = 'prueba.prueba'
    _description = 'prueba.prueba'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()

    @api.depends('value')
    def _value_pc(self):        
        for record in self:
            record.value2 = float(record.value) / 100
            
            servidor = 'Servertao\CONTPAQ'
            db = 'nomGenerales'
            uid = 'sa'
            passwo = 'syssql'
            try:
                conexion = pymssql.connect(servidor,uid,passwo,db)
                record.description = 'Conexion exitosa'
            except Exception as e:
                record.description = str(e)
