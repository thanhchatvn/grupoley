# -*- coding: utf-8 -*-

{
    'name': 'POS Client List with reference',
    'version': '1.0.1',
    'category': 'Sales/Point of Sale',
    'sequence': 10,
    'summary': 'Inherit ticket POS ',
     'author': "DataWorks",
    'description': "",
    'depends': ['base','point_of_sale'],
    'data': [
         'views/templates.xml',

    ],
    'demo': [

    ],
    'installable': True,
    'application': True,
    'qweb': [
        'static/src/xml/ClientLine.xml',
        'static/src/xml/ClientListScreen.xml',

    ],
    'website': '',
}
