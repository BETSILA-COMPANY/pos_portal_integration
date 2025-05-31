# -*- coding: utf-8 -*-
{
    'name': 'POS Portal Integration',
    'version': '16.0.1.0.0',
    'summary': 'Allow portal users to order products available in POS from their customer portal.',
    'description': """
        This module integrates Odoo's Point of Sale (POS) with the customer portal, allowing:

        - Registered portal users to browse products marked 'Available in PoS'.
        - Customers to create and submit new POS orders directly from their personalized portal account.
        - Automated creation of submitted orders as Draft POS Orders in the Odoo backend.
        - POS staff to efficiently process portal-submitted orders.
        - Enhances customer convenience and streamlines order management.
        (This content is typically overridden by description/index.html on the App Store, but good for internal Odoo description)
    """,
    'category': 'Sales/Point of Sale', # More specific category is good
    'author': 'BETSILA AND COMPANY',
    'website': 'https://www.yourcompany.com', # IMPORTANT: Add your actual website URL here
    'license': 'LGPL-3',
    'depends': [
        'point_of_sale',
        'product',
        'base',
        'website',
        'portal',
        'sale',
        # Consider 'website_portal' and 'website_sale' if your portal relies heavily on them for structure/login
        # 'website_portal',
        # 'website_sale',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'views/pos_order_views.xml',
        'views/product_views.xml',
        'views/portal_templates.xml',
        'views/pos_templates.xml',
    ],
    'assets': {
        # These assets load in the Odoo backend POS interface
        'point_of_sale.assets': [
            # Only include JS files here that are specifically for the POS backend UI
            # e.g., if you have modifications to the POS client itself to handle portal orders
            # If 'pos_portal_orders.js' and 'portal_order_loader.js' are meant for the backend, keep them here.
            # Otherwise, move them to web.assets_frontend.
            # Example: 'pos_portal_integration/static/src/js/pos_backend_logic.js',
        ],
        # These assets load on the website frontend (portal)
        'web.assets_frontend': [
            '/pos_portal_integration/static/src/css/portal_pos.css', # If you have a custom CSS file
            '/pos_portal_integration/static/src/js/portal_order_loader.js', # If this loads frontend logic
            '/pos_portal_integration/static/src/js/pos_portal_orders.js',   # If this loads frontend logic
            '/pos_portal_integration/static/src/js/portal_pos.js',          # Your existing frontend JS
        ],
    },
    'images': [
        'static/description/icon.png', # Your module's icon
        'static/description/banner.png', # Optional: A banner image for the top of the listing
        'static/description/index.html',
        'static/description/develop_1.png',
        'static/description/develop_2.png',
        'static/description/develop_3.png',
        'static/description/develop_4.png',
        'static/description/develop_5.png',
        'static/description/develop_6.png',
    ],
    'installable': True,
    'application': True, # Mark as an application if it's a major feature, not just a small technical module
    'auto_install': False,
    'price': 250.00,
    'currency_id': 'USD',
}
