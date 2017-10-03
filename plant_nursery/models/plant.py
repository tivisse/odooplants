# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError


class Plants(models.Model):
    _name = 'nursery.plant'

    name = fields.Char("Plant Name")
    price = fields.Float()
    order_ids = fields.One2many("nursery.order", "plant_id", string="Orders")
    order_count = fields.Integer(compute='_compute_order_count',
                                 store=True,
                                 string="Total sold")
    number_in_stock = fields.Integer()

    @api.depends('order_ids')
    def _compute_order_count(self):
        for plant in self:
            plant.order_count = len(plant.order_ids)

    @api.constrains('order_count', 'number_in_stock')
    def _check_available_in_stock(self):
        for plant in self:
            if plant.number_in_stock and \
              plant.order_count > plant.number_in_stock:
                raise UserError("There is only %s %s in stock but %s were sold"
                      % (plant.number_in_stock, plant.name, plant.order_count))
