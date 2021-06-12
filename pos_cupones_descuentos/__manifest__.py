# -*- coding: utf-8 -*-

{
    "name": "Point of Sale Coupons",
    "version": "1.0",
    "category": "Sales/Point Of Sale",
    "sequence": 6,
    "summary": "Use coupons in Point of Sale",
    "description": "",
    "depends": ["coupon", "point_of_sale"],
    "data": [
        "data/mail_template_data.xml",
        'data/default_barcode_patterns.xml',
        'data/data.xml',
        "security/ir.model.access.csv",
        "views/coupon_views.xml",
        "views/coupon_program_views.xml",
        "views/pos_config_views.xml",
        "views/res_config_settings_views.xml",
        'views/templates.xml',
        'views/product_views.xml',
        ],

    "qweb": [
        'static/src/xml/ControlButtons/PromoCodeButton.xml',
        'static/src/xml/ControlButtons/ResetProgramsButton.xml',
        'static/src/xml/ActivePrograms.xml',
        'static/src/xml/OrderReceipt.xml',
        'static/src/xml/OrderWidget.xml'
    ],

}
