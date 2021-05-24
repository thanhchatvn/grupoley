# -*- coding: utf-8 -*-
{
    'name': "PDV Impresion Ticket",
    'version': '1.0',
    'depends': [
        'point_of_sale',
    ],
    'author': "DataWorks",
    'category': 'Custom',
    'description': "Personalizacion para agregar Impresion Ticket en el PDV",
    'summary': "Personalizacion para agregar Impresion Ticket en el PDV",

    'data': [
        'views/pos_config_views.xml',
        'views/templates.xml',
    ],

    'qweb': [
        'static/src/xml/Screens/ProductScreen/ControlButtons/PrintBillButton.xml',
        'static/src/xml/Screens/ImprimirTicketScreen.xml',
    ],
}
