# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class Order(models.Model):
    _name = 'plant.order'
    _description = 'Plant Order'
    _order = 'id DESC'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'rating.mixin', 'utm.mixin']

    name = fields.Char(
        'Reference', default=lambda self: _('New'),
        required=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible',
        index=True, required=True,
        default=lambda self: self.env.user)
    date_open = fields.Date(
        'Confirmation date', readonly=True)
    customer_id = fields.Many2one(
        'plant.customer', string='Customer',
        index=True, required=True)
    line_ids = fields.One2many(
        'plant.order.line', 'order_id', string='Order Lines')
    amount_total = fields.Integer(
        'Amount', compute='_compute_amount_total', store=True)
    company_id = fields.Many2one(
        'res.company', string='Company', related='user_id.company_id',
        reaodnly=True, store=True)
    currency_id = fields.Many2one(
        'res.currency', string='Currency', related='company_id.currency_id',
        readonly=True, required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('done', 'Done'),
        ('cancel', 'Canceled')], string='State',
        default='draft', index=True, required=True)

    @api.depends('line_ids.price')
    def _compute_amount_total(self):
        for order in self:
            order.amount_total = sum(order.mapped('line_ids.price'))

    def action_confirm(self):
        if self.state != 'draft':
            return
        return self.write({
            'state': 'open',
            'date_open': fields.Datetime.now(),
        })

    def action_get_ratings(self):
        action = self.env['ir.actions.act_window'].for_xml_id('rating', 'action_view_rating')
        return dict(
            action,
            domain=[('res_id', 'in', self.ids), ('res_model', '=', 'plant.order')],
        )

    def action_send_rating(self):
        rating_template = self.env.ref('plant_nursery.mail_template_plant_order_rating')
        for order in self:
            order.rating_send_request(rating_template, force_send=True)


class OrderLine(models.Model):
    _name = 'plant.order.line'
    _description = 'Plant Order Line'
    _order = 'order_id DESC'
    _rec_name = 'order_id'

    order_id = fields.Many2one(
        'plant.order', string='Order',
        index=True, ondelete='cascade', required=True)
    plant_id = fields.Many2one(
        'plant.plant', string='Plant',
        index=True, ondelete='cascade', required=True)
    price = fields.Float('Price')

    @api.onchange('plant_id')
    def _onchange_plant_id(self):
        if self.plant_id:
            self.price = self.plant_id.price

    def create(self, values):
        if 'price' not in values:
            values['price'] = self.env['plant.plant'].browse(values['plant_id']).price
        return super(OrderLine, self).create(values)
