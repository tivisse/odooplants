# -*- coding: utf-8 -*-

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
            'user': request.env.user,
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
            'user': request.env.user,
            'plants': plants,
            'search': post,
        }

        return request.render("plant_nursery.portal_plants", values)

    @route('/plant/<int:plant_id>', type='http', auth="public", website=True)
    def plant(self, plant_id, **post):
        values = {
            'company': request.env.user.company_id.sudo(),
            'plant': request.env['plant.plant'].browse(plant_id),
        }

        return request.render("plant_nursery.portal_plant_page", values)
