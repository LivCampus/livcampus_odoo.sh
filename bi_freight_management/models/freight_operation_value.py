# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class FreightOperation(models.Model):
    _name = 'freight.operation.value'
    _description = 'Freight Operation'

    name = fields.Char(string='name', required=True)
