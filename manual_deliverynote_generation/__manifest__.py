{
    'name': 'Manual Delivery Note',
    'version': '15.0.1.0.0',
    'summary': 'Create and manage manual delivery notes from Sales Orders',
    'description': """
<div class="oe_structure">
    <div class="oe_title">
        <i class="fa fa-truck"></i>
        Manual Delivery Note
    </div>

    <div class="oe_paragraph">
        Create and manage <strong>manual delivery notes</strong> directly from 
        <strong>Sales Orders</strong>. This module seamlessly integrates with 
        <strong>Sales</strong> and <strong>Inventory</strong> to give you full control 
        over delivery documentation.
    </div>

    <div class="oe_subtitle">
        <i class="fa fa-star"></i>
        Key Features
    </div>
    <ul class="oe_list">
        <li>Manual delivery note creation</li>
        <li>Direct integration with Sales Orders</li>
        <li>Fully compatible with Odoo Inventory</li>
    </ul>

    <div class="oe_subtitle">
        <i class="fa fa-cogs"></i>
        Business Benefits
    </div>
    <ul class="oe_list">
        <li>Better control over delivery documentation</li>
        <li>Improved sales and logistics coordination</li>
        <li>Reduced dependency on automatic delivery flows</li>
    </ul>
</div>
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
