# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class FreightPackage(models.Model):
    _name = 'freight.package'
    _description = 'Freight Package'

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True)
    is_container = fields.Boolean(string='Container', default=False)
    refrigerate = fields.Boolean(string='Refrigerate', default=False)
    size = fields.Float(string='Size', required=True)
    volume = fields.Float(string='Volume', required=True)
    active = fields.Boolean(string='Active', default=True)
