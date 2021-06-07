# -*- coding: utf-8 -*-

from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    promissory_note = fields.text(
    )

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

