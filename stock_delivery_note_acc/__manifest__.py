# -*- coding: utf-8 -*-
{
    'name': "stock_delivery_note_acc",

    'summary': """
        Formatos de vale de entrega con contabilizacion y sin contabilizacion
    """,

    'description': """
         Formatos de vale de entrega con contabilizacion y sin contabilizacion
    """,

    'author': "",

    'website': "https://todoo.grupoley.com.mx",


    'category': 'Inventory',

    'version': '1.0.1',

    'depends': ['base','stock','purchase_order_report'],
    'css':'static/src/css/invoice-style.css',

    'data': [
        'views/item_web.xml',
        'reports/delivery_note_report_acc.xml',

    ],

    'demo': [
    ],
}