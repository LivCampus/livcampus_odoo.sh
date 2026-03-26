# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class FreightTracking(models.Model):
    _name = 'freight.tracking'
    _description = 'Freight Tracking'

    location = fields.Char(string='Location', required=True)
    description = fields.Char(string='Description', required=True)
    date = fields.Date(string='Date')
    freight_operation_id = fields.Many2one('freight.operation', string='Freight Operation')
