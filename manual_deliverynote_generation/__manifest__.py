{
    'name': 'Manual Delivery Note',
    'version': '15.0.1.0.0',
    'summary': 'Create and manage manual delivery notes from Sales Orders',
    'description': """
Manual Delivery Note
====================
This module allows users to create and manage manual delivery notes
directly from Sales Orders. It integrates with Sales and Inventory
to provide better control over delivery documentation.

Key Features:
-------------
- Manual delivery note creation
- Integration with Sales Orders
- Compatible with Odoo Inventory
""",


    'category': 'Sales',
    'author': 'Acugence Systems Pvt Ltd',
    'maintainer': 'Acugence Systems Pvt Ltd',
    'website': 'https://www.acugence.qa',
    'license': 'LGPL-3',
    'price': 0.0,
    'currency': 'USD',
    'depends': [
        'sale',
        'stock',
        'sale_stock',
    ],
    'data': [
        'views/sale_order_views.xml',
    ],
    'images': [
        'static/description/banner.jpg',
        'static/description/icon.png',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
