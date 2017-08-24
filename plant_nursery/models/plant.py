# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, exceptions, fields, models, _


class Category(models.Model):
    _name = 'plant.category'
    _description = 'Plant Category'
    _order = 'name'

    name = fields.Char('Name', required=True)


class Tag(models.Model):
    _name = 'plant.tag'
    _description = 'Plant Tag'
    _order = 'name'

    name = fields.Char('Name', required=True)
    color = fields.Integer('Color Index', default=10)


class Plants(models.Model):
    _name = 'plant.plant'
    _description = 'Plant'
    _order = 'name'

    name = fields.Char('Plant Name', required=True)
    # description
    description_short = fields.Html('Short description')
    description = fields.Html('Description')
    category_id = fields.Many2one('plant.category', string='Category')
    image = fields.Binary('Photo', attachment=True)
    tag_ids = fields.Many2many('plant.tag', string='Tags')
    # sell
    user_id = fields.Many2one(
        'res.users', string='Responsible',
        index=True, required=True,
        default=lambda self: self.env.user)
    stock = fields.Integer('Stock')
    price = fields.Float('Price')

    @api.constrains('stock')
    def _check_stock(self):
        if self.stock < 0:
            raise exceptions.ValidationError(
                _('Stock cannot be negative.')
            )
