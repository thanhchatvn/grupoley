# -*- coding: utf-8 -*-
{
    'name': "POS Promotions",
    'version': '1.0',
    'depends': [
        'point_of_sale',
    ],
    'author': "DataWorks",
    'category': 'Point of Sale',
    'description': "Personalizacion para manejo de promociones y descuentos POS",
    'summary': "Personalizacion para manejo de promociones y descuentos POS",

    'data': [
        #'views/pos_config_views.xml',
        'views/templates.xml',
    ],

    'qweb': [
         'static/src/xml/pos_product_screen.xml',
        #'static/src/xml/Screens/ProductScreen/ControlButtons/CustomPosPromotion.xml',
    ],
}
