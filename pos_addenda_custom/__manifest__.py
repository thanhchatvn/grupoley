# -*- coding: utf-8 -*-
{
    'name': "PDV Addenda",
    'version': '1.0',
    'depends': [
        'point_of_sale',
        'account',
        'l10n_mx_edi',
        'partner_addenda',
    ],
    'author': "DataWorks",
    'category': 'Custom',
    'description': "Personalizacion para agregar Addenda en el PDV",
    'summary': "Personalizacion para agregar Addenda en el PDV",

    'data': [
        'views/templates.xml',
    ],

    'qweb': [
        'static/src/xml/Screens/PaymentScreen/PaymentScreen.xml',
        'static/src/xml/Popups/AdendaPopup.xml'
    ],
}
