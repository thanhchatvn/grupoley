# -*- coding: utf-8 -*-

{
    "name" : "Internal Stock Transfer for Different Warehouse",
    "author": "Edge Technologies",
    "version" : "14.0.1.0",
    "live_test_url":'https://youtu.be/OQxi5Q7neRI',
    "images":["static/description/main_screenshot.png"],
    'summary': 'Stock Internal Transfer for Warehouse stock transfer stock for different warehouse transfer stock for internal warehouse stock transfer for internal location warehouse stock internal transfer internal stock transfer for one warehouse to another warehouse',
    "description": """ 
    This apps helps user to transfer stock from one Warehouse to another Warehouse
    """, 
    "license" : "OPL-1",
    "depends" : ['base','stock'],
    "data": [
        'security/stock_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'wizard/stock_product_produce_views.xml',
        'views/stock_transfer_views.xml',
        'report/internal_template.xml',
        'report/internal_transfer_action.xml',
        'report/receipt_template.xml',
        'report/receipt_report.xml',
        'report/filter_view.xml',
        'report/filter_template.xml',
        'report/filter_action.xml',
        ],
    "auto_install": False,
    "installable": True,
    "price": 25,
    "currency": 'EUR',
    "category" : "Warehouse",
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
