# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class FreightAirlineIcao(models.Model):
    _name = 'freight.airline.icao'
    _description = 'Freight Airline ICAO'

    name = fields.Char(string='Name', required=True)
    country_id = fields.Many2one('res.country', string='Country')
    freight_airline_ids = fields.One2many('freight.airline', 'icao_id', string='Airlines')


class FreightAirline(models.Model):
    _name = 'freight.airline'
    _description = 'Freight Airline'

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True)
    country_id = fields.Many2one('res.country', string='Country')
    icao_id = fields.Many2one('freight.airline.icao', string='ICAO')
    active = fields.Boolean(string='Active', default=True)
