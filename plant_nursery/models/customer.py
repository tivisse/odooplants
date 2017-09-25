# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Customer(models.Model):
    _name = 'plant.customer'
    _description = 'Customer'
    _order = 'name'
    _inherit = ['mail.thread']

    name = fields.Char('Name', required=True)
    email = fields.Char('Email')
    image = fields.Binary('Photo', attachment=True)
    # address
    address = fields.Char('Address')
    country_id = fields.Many2one('res.country', string='Country')

    def find_or_create(self, name, email):
        customer = self.search(['|', ('name', '=', name), ('email', '=', email)])
        if not customer:
            customer = self.create({'name': name, 'email': email})
        elif customer.name != name:
            customer.write({'name': name})
        elif customer.email != email:
            customer.write({'email': email})
        return customer
