# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Plant Nursery Data',
    'version': '1.0',
    'category': 'Hidden',
    'summary': 'Data for Plant Nursery',
    'depends': ['plant_nursery', 'mail'],
    'data': [
        'data/base_data.xml',
        'data/customer_data.xml',
        'data/plant_data.xml',
        'data/order_data.xml',
        'data/mail_data.xml', #THIS FILE IS NOT COMMITTED
    ],
    'demo': [
    ],
    'css': [],
    'auto_install': False,
    'application': False,
}
