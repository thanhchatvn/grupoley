# -*- coding: utf-8 -*-
{
    'name': "stock_deliveryslip_report_custom",
    'summary': """
        Ajustes Formato de vale de entrega nativo
    """,

    'description': """
         Formatos de vale de entrega nativo con ajuste en traduccion
    """,

    'author': "Dataworks",

    'website': "https://todoo.grupoley.com.mx",


    'category': 'Inventory',

    'version': '1.0.1',

    'depends': ['base','stock','purchase_order_report'],
    'css':'static/src/css/invoice-style.css',

    'data': [
        'report/inherit_report_deliveryslip.xml',
        #'report/inherit_tcall_repor_table_detail.xml',
    ],

    'demo': [
    ],
}