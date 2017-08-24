# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Customer(models.Model):
    _name = 'nursery.customer'

    name = fields.Char("Customer Name", required=True)
    email = fields.Char(help="To receive the newsletter")
