# -*- coding: utf-8 -*-

import random

from odoo.http import Controller, request, route


class TripController(Controller):

    # Generic display pages
    # --------------------------------------------------

    @route('/hello', type='http', auth="public", website=True)
    def plants_hello(self, **post):
        return request.render("plant_nursery.plant_hello", {'name': 'World'})

    @route('/hello2', type='http', auth="public", website=True)
    def plants_hello2(self, **post):
        return request.render("plant_nursery.plant_hello2", {'name': 'World'})

    @route('/hello3', type='http', auth="public", website=True)
    def plants_hello3(self, **post):
        values = {
            'company': request.env.user.company_id.sudo(),
            'plants': request.env['plant.plant'].search([]),
        }
        return request.render("plant_nursery.plant_hello3", values)

    @route(['/plants', '/plants/page/<int:page>'], type='http', auth="public", website=True)
    def plants(self, page=1, **post):
        plant_domain = []
        if post.get('category'):
            plant_domain += [('category_id.name', 'ilike', post['category'])]
        plants = request.env['plant.plant'].search(plant_domain)

        values = {
            'company': request.env.user.company_id.sudo(),
            'plants': plants,
            'search': post,
        }
        if post.get('order_id'):
            values['order'] = request.env['plant.order'].browse(int(post['order_id']))

        return request.render("plant_nursery.portal_plants", values)

    @route('/plants/quote', type='http', auth="public", website=True)
    def plants_quote(self, **post):
        customer_name = post.get('customer_name')
        customer_email = post.get('customer_email')
        if not customer_name and not customer_email:
            return request.redirect('/plants')

        line_ids = []
        for key, value in post.items():
            if key.startswith('free_'):
                free_id = int(key.split('free_')[1])
                reduc = post.get('reduc_free_%s' % free_id)
                line_ids.append((0, 0, {
                    'plant_id': free_id,
                    'price': 0,
                }))
            elif key.startswith('promo_'):
                promo_id = int(key.split('promo_')[1])
                reduc = int(post.get('reduc_promo_%s' % promo_id))
                line_ids.append((0, 0, {
                    'plant_id': promo_id,
                    'price': request.env['plant.plant'].browse(promo_id).price * ((100 - reduc) * 0.01),
                }))

        if line_ids:
            customer = request.env['plant.customer'].find_or_create(customer_name, customer_email)
            order = request.env['plant.order'].create({
                'customer_id': customer.id,
                'line_ids': line_ids,
            })
            return request.redirect('/plants?order_id=%s' % order.id)

        return request.redirect('/plants')

    @route('/plant/<int:plant_id>', type='http', auth="public", website=True)
    def plant(self, plant_id, **post):
        values = {
            'company': request.env.user.company_id.sudo(),
            'plant': request.env['plant.plant'].browse(plant_id),
        }

        return request.render("plant_nursery.portal_plant_page", values)

    # Live update
    # --------------------------------------------------

    @route(['/plant/get_random_quote'], type='json', auth="public", website=True)
    def get_plants_availability_data(self):
        plant_domain = [('stock', '>', 0)]
        plants = request.env['plant.plant'].search(plant_domain)

        random.seed()
        promo = random.randrange(20, 80, 10)

        plant = request.env['plant.plant'].browse([random.choice(plants.ids)])
        free = request.env['plant.plant'].browse([random.choice(plants.ids)])

        return {
            'promo': [{
                'plant': plant.name,
                'plant_id': plant.id,
                'promo': promo,
            }],
            'free': [{
                'plant': free.name,
                'plant_id': free.id,
                'promo': 100,
            }],
        }
