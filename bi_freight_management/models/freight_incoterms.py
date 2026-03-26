# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class FreightIncoterms(models.Model):
    _name = 'freight.incoterms'
    _description = 'Freight Incoterms'

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(string='Active', default=True)
