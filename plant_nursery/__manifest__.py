# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Plant Nursery',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Plants and Customers Management',
    'depends': ['web'],
    'data': [
        'security/ir.model.access.csv',
        'views/nursery_plant_views.xml',
        'views/nursery_customer_views.xml',
    ],
    'demo': [
    ],
    'css': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
