# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import uuid

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
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    def _get_default_access_token(self):
        return str(uuid.uuid4())

    name = fields.Char('Plant Name', required=True)
    # description
    description_short = fields.Html('Short description')
    internal = fields.Boolean('Internal')
    access_token = fields.Char(
        'Security Token', copy=False,
        default=_get_default_access_token)
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

    def _compute_portal_url(self):
        for plant in self:
            plant.portal_url = '/plant/%s?access_token=%s' % (plant.id, plant.access_token)

    @api.constrains('stock')
    def _check_stock(self):
        if self.stock < 0:
            raise exceptions.ValidationError(
                _('Stock cannot be negative.')
            )

    @api.model_cr_context
    def _init_column(self, column_name):
        """ Initialize the value of the given column for existing rows.

            Overridden here because we need to generate different access tokens
            and by default _init_column calls the default method once and applies
            it for every record.
        """
        if column_name != 'access_token':
            super(Plants, self)._init_column(column_name)
        else:
            query = """UPDATE %(table_name)s
                          SET %(column_name)s = md5(md5(random()::varchar || id::varchar) || clock_timestamp()::varchar)::uuid::varchar
                        WHERE %(column_name)s IS NULL
                    """ % {'table_name': self._table, 'column_name': column_name}
            self.env.cr.execute(query)
