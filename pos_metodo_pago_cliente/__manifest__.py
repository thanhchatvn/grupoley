# -*- coding: utf-8 -*-
{
    'name': "PDV Metodo pago por cliente",
    'version': '1.0',
    'depends': [
        'point_of_sale',
        'account',
        'res_partner_cfdi',
    ],
    'author': "DataWorks",
    'category': 'Custom',
    'description': "Personalizacion para limitar Metodo pago por cliente por cliente en el PDV",
    'summary': "Personalizacion para limitar Metodo pago por cliente por cliente en el PDV",

    'data': [
        'views/templates.xml',
    ],

    'qweb': [
        'static/src/xml/Screens/PaymentScreen/PaymentScreen.xml',
    ],
}
