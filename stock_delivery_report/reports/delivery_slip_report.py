# -*- coding: utf-8 -*-

from odoo import api, models, _
from odoo.exceptions import ValidationError, UserError, RedirectWarning
import dateutil.parser
import datetime

class DeliverySlipCustomReport(models.Model):
    _name = 'report.stock_delivery_report.report_multiple_delivery_slip'
    _description = 'Multiples purchase orders and one delivery slip'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['stock.picking'].browse(docids)

        # Folio que nos ayudara a filtrar nuestros registros
        folio_filter = ""   
        partner_filter = ""

        # Asignamos el valor a nuestro filtro desde nuestro registro seleccionado
        for i, record in enumerate(docs):
            # Si se seleccionó solo un registro
            if i == 0:
                folio_filter = record.x_order_folio
                partner_filter = record.partner_id.id
                if record.date_done:
                    effective_year = int(record.date_done.year)
                    effective_month = int(record.date_done.month)
                    effective_day = int(record.date_done.day)
                    initial_effective_date = datetime.datetime(effective_year,effective_month,effective_day,0,0)
                    final_effective_date = datetime.datetime(effective_year,effective_month,effective_day,23,59,59)
                else:
                    effective_year = int(record.scheduled_date.year)
                    effective_month = int(record.scheduled_date.month)
                    effective_day = int(record.scheduled_date.day)
                    initial_effective_date = datetime.datetime(effective_year,effective_month,effective_day,0,0)
                    final_effective_date = datetime.datetime(effective_year,effective_month,effective_day,23,59,59)
                    
                
            # Si se seleccionó más de un registro
            elif i > 0:
                raise UserError(_("It is not possible to generate the report, only a delivery slip must be selected"))
            else:
                pass

        # Agrupamos los registros por medio del folio 
        if record.date_done:
            records = self.env['stock.picking'].search(['&','&','&',('date_done','>=',initial_effective_date), ('date_done','<=',final_effective_date),('partner_id','=',partner_filter),('x_order_folio','=',folio_filter)])
        else:
            records = self.env['stock.picking'].search(['&','&','&',('scheduled_date','>=',initial_effective_date), ('scheduled_date','<=',final_effective_date),('partner_id','=',partner_filter),('x_order_folio','=',folio_filter)])

        return {
            'docs':docs,
            'records': records,
        }