# -*- coding: utf-8 -*-
{
    'name': "PDV Autorizacion",
    'version': '1.0',
    'depends': [
        'point_of_sale',
        'account',
        'account_followup',
    ],
    'author': "DataWorks",
    'category': 'Custom',
    'description': "Personalizacion para agregar Autorizacion en el PDV",
    'summary': "Personalizacion para agregar Autorizacion en el PDV",

    'data': [
        'security/ir.model.access.csv',
        'views/point_of_sale_view.xml',
        'views/templates.xml',
        'views/pos_autorizacion_views.xml',
    ],

    'qweb': [

    ],
}
