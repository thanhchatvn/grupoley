# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class invoice_pdf_customization(models.Model):
#     _name = 'invoice_pdf_customization.invoice_pdf_customization'
#     _description = 'invoice_pdf_customization.invoice_pdf_customization'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class AccountInvoice(models.Model):
    _inherit = 'account.move'

    def calculate_cfdi_values_pdf(self):
        self.ensure_one()
        invoice = self.sudo()
        cfdi_values = {}
        for line in invoice.invoice_line_ids:
            if not line.product_id:
                continue
            cfdi_values[line.id] = {}
            cfdi_values[line.id]['wo_discount'] = line.price_unit * (1 - (line.discount / 100.0))

            cfdi_values[line.id]['discount_rate'] = (line.sale_line_ids.discount_original) if line.sale_line_ids.discount_rate  else  line.sale_line_ids.discount
            cfdi_values[line.id]['discount_promotion'] = (line.sale_line_ids.discount_promotions) if line.sale_line_ids.discount_promotions else 0

            cfdi_values[line.id]['discount_amount_price_list'] = (line.quantity * line.price_unit) * (cfdi_values[line.id]['discount_rate']/100.0)
            cfdi_values[line.id]['discount_amount']  = (line.quantity * line.price_unit) * (cfdi_values[line.id]['discount_promotion']/100.0)


            cfdi_values[line.id]['total_wo_discount'] = invoice.currency_id.round((line.price_unit * line.quantity) - (cfdi_values[line.id]['discount_amount_price_list'] + cfdi_values[line.id]['discount_amount']))
            cfdi_values[line.id]['price_subtotal_unit'] = invoice.currency_id.round(
                cfdi_values[line.id]['total_wo_discount'] / line.quantity)
        return cfdi_values

    def get_footer_values(self):
        invoice = self.sudo()
        response = {}
        promissory_note = """POR ESTE PAGARE ME(NOS) OBLIGO(AMOS) A PAGAR INCONDICIONALMENTE, A LA ORDEN DE INDUSTRIAS 
        GUACAMAYA SA DE CV, EL DÍA """+str(self.invoice_date)+""", EN ESTA CIUDAD, O EN CUALQUIER OTRA QUE SEA(MOS) 
        REQUERIDO(OS) A ELECCION DEL TENEDOR DE ESTE PAGARE EL DIA DEL VENCIMIENTO INDICADO, LA CANTIDAD DE, 
        """+str(self.amount_residual)+""" ( """+ invoice._l10n_mx_edi_cfdi_amount_to_text() +"""" ), VALOR RECIBIDO 
        EN MERCANCIA. """

        reiterate =  """(NUESTRA) ENTERA SATISFACCION, SI NO FUERE PUNTUALMENTE CUBIERTO A SU VENCIMIENTO, PAGARE 
        INTERESES MORATORIOS HASTA SU LIQUIDACION TOTAL A RAZON DEL % MENSUAL CULIACÁN SINALOA, A """+str(self.invoice_date)

        response['promissory_note'] = promissory_note
        response['reiterate'] = reiterate

        return response

    def is_invoice_client(self):
        invoice = self
        if 'in_invoice' in invoice.move_type:
            return False
        if 'out_invoice' in invoice.move_type:
            return True

    def calculate_lines_details(self):
        self.ensure_one()
        invoice = self.sudo()
        details_move_lines = {}

        code_iva = "14020001"
        subtotal_products = 0
        subtotal_iva = 0
        subtotal_credit = 0

        total_debit = 0
        total_credit = 0

        details_move_lines["details_product"] = []
        details_move_lines["details_tax"] = []
        details_move_lines["details_credit"] = []
        details_move_lines["details_credit"] = []
        for line in invoice.line_ids:
            #extraccion de detalles del producto
            if line.product_id:
               subtotal_products = subtotal_products + line.debit
               details_move_lines["details_product"].append(line)
            #Extracción para los detalles de iva
            elif not line.product_id and line.tax_line_id:
                subtotal_iva = subtotal_iva + line.debit
                details_move_lines["details_tax"].append(line)
            #Exctracción de otros conceptos
            elif not line.product_id and not line.tax_line_id:
                subtotal_credit = subtotal_credit + line.credit
                details_move_lines["details_credit"].append(line)

        total_debit = subtotal_products + subtotal_iva
        total_credit = subtotal_credit
        details_move_lines.update({"subtotal_products": subtotal_products})
        details_move_lines.update({"subtotal_tax" : subtotal_iva})
        details_move_lines.update({"total_debit" : total_debit})
        details_move_lines.update({"total_credit": total_credit})

        return details_move_lines

    def calculate_no_entrada(self):
        #se obtiene el ultimo insertado según las fechas
        response = self.env["stock.picking"].search([('origin','=',self.invoice_origin),('partner_id','=',self.partner_id.id),('date_done', '<=',self.invoice_date)], order= 'date_done desc', limit=1)
        if response:
            return response
        return {}
