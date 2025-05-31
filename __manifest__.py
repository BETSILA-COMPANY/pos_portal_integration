# -*- coding: utf-8 -*-
{
    'name': 'POS Portal Integration',
    'version': '16.0.1.0.0',
    'summary': 'Allow portal users to order products available in POS',
    'description': """
        This module integrates POS with the customer portal, allowing:
        - Portal users to view and order POS products
        - POS users to process portal-submitted orders
    """,
    'category': 'Point of Sale',
    'author': 'BETSILA AND COMPANY',
    'license': 'LGPL-3',
    'depends': ['point_of_sale', 'product', 'base',  'website',  'portal', 'sale', ],
    'data': [
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'views/pos_order_views.xml',
        'views/product_views.xml',
        'views/portal_templates.xml',
        'views/pos_templates.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'pos_portal_integration/static/src/js/pos_portal_orders.js',
            'pos_portal_integration/static/src/js/portal_order_loader.js'
        ],
        'web.assets_frontend': [
            'pos_portal_integration/static/src/js/portal_pos.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
