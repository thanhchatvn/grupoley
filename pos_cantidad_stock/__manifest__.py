# -*- coding: utf-8 -*-
{
    'name': "PDV Stock",
    'version': '1.0',
    'depends': [
        'point_of_sale',
        'account',
        'l10n_mx_edi',
    ],
    'author': "DataWorks",
    'category': 'Custom',
    'description': "Personalizacion para agregar Stock en el PDV",
    'summary': "Personalizacion para agregar Stock en el PDV",

    'data': [
        'views/pos_assets_common.xml',
        'views/pos_config_views.xml',
    ],

    'qweb': [
        'static/src/xml/Screens/ProductScreen/ProductItem.xml',
        'static/src/xml/Screens/ProductScreen/ProductsWidgetControlPanel.xml',
    ],
}
