{
    'name': 'Manual Delivery Note',
    'version': '15.0.1.0.0',
    'summary': 'Create and manage manual delivery notes from Sales Orders',
    'description': """
<div class="oe_container">
    <section class="oe_row oe_spaced">
        <h2 class="oe_slogan">
            <i class="fa fa-truck"></i>
            Manual Delivery Note
        </h2>
        <p class="oe_mt32 text-center">
            Create and manage <strong>manual delivery notes</strong> directly from
            <strong>Sales Orders</strong>. This module seamlessly integrates with
            <strong>Sales</strong> and <strong>Inventory</strong> to give you full
            control over delivery documentation.
        </p>
    </section>

    <section class="oe_row oe_spaced">
        <h3 class="oe_slogan">
            <i class="fa fa-star"></i>
            Key Features
        </h3>
        <ul class="oe_mt32">
            <li>
                <i class="fa fa-check-circle text-success"></i>
                Manual delivery note creation
            </li>
            <li>
                <i class="fa fa-check-circle text-success"></i>
                Direct integration with Sales Orders
            </li>
            <li>
                <i class="fa fa-check-circle text-success"></i>
                Fully compatible with Odoo Inventory
            </li>
        </ul>
    </section>

    <section class="oe_row oe_spaced">
        <h3 class="oe_slogan">
            <i class="fa fa-cogs"></i>
            Business Benefits
        </h3>
        <ul class="oe_mt32">
            <li>
                <i class="fa fa-arrow-right"></i>
                Better control over delivery documentation
            </li>
            <li>
                <i class="fa fa-arrow-right"></i>
                Improved sales and logistics coordination
            </li>
            <li>
                <i class="fa fa-arrow-right"></i>
                Reduced dependency on automatic delivery flows
            </li>
        </ul>
    </section>
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
        'static/description/banner.png',
        'static/description/icon.png',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
