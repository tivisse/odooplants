# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Plant Nursery',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Plants and customers management',
    'description': 'So Much Plants',
    'depends': ['web', 'http_routing'],
    'data': [
        'data/plant_data.xml',
        'views/plant_menus.xml',
        'views/order_views.xml',
        'views/plant_views.xml',
        'views/customer_views.xml',
        'views/assets.xml',
        'views/plant_portal_templates.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
    ],
    'css': [],
    'auto_install': False,
    'application': True,
}
