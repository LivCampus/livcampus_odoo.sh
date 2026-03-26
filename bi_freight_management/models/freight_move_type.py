# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class FreightMoveType(models.Model):
    _name = 'freight.move.type'
    _description = 'Freight Move Type'

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(string='Active', default=True)