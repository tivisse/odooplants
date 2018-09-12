# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Customer(models.Model):
    _name = 'nursery.customer'
    _description = 'Customer'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Customer Name", required=True)
    email = fields.Char(help="To receive the newsletter")
    image = fields.Binary('Photo', attachment=True)
    address = fields.Char('Address')
    country_id = fields.Many2one('res.country', string='Country')
