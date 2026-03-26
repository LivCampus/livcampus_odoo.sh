# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class FreightPort(models.Model):
    _name = 'freight.port'
    _description = 'Freight Port'

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True)
    country_id = fields.Many2one('res.country', string='Country')
    fed_state_id = fields.Many2one('res.country.state', string='Fed. State')
    air = fields.Boolean(string='Air', default=True)
    ocean = fields.Boolean(string='Ocean', default=True)
    land = fields.Boolean(string='Land', default=True)
    active = fields.Boolean(string='Active', default=True)
