# -*- coding: utf-8 -*-
{
    'name': "PDV Lista de Precios",
    'version': '1.0',
    'depends': [
        'point_of_sale',
        'pos_restaurant',
    ],
    'author': "DataWorks",
    'category': 'Custom',
    'description': "Personalizacion para limitar Lista de precios por cliente en el PDV",
    'summary': "Personalizacion para limitar Lista de precios por cliente en el PDV",

    'data': [
        'views/pos_assets_common.xml',
        'views/pos_config_views.xml',
    ],

    'qweb': [
        'static/src/xml/Screens/ClientListScreen/ClientLine.xml',
        'static/src/xml/Screens/ClientListScreen/ClientDetailsEdit.xml',
    ],
}
