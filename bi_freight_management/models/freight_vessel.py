# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class FreightVessel(models.Model):
    _name = 'freight.vessel'
    _description = 'Freight Vessel'

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True)
    country_id = fields.Many2one('res.country', string='Country')
    global_zone_id = fields.Many2one('res.country.group', string='Global Zone')
    active = fields.Boolean(string='Active', default=True)