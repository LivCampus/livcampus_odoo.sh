# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class FreightOrderPackageItem(models.Model):
    _name = 'freight.order.package.item'
    _description = 'Freight Order Package Item'

    description = fields.Char(string='Description', required=True)
    package_id = fields.Many2one(
        'freight.package', string='Package', required=True)
    quantity = fields.Float(string='Quantity', required=True)
    operation_value_id = fields.Many2one('freight.operation.value', string='Operation')
    volume = fields.Float(string='Volume(CBM)', required=True)
    gross_weight = fields.Float(string='Gross Weight(KG)', required=True)
    freight_order_package_id = fields.Many2one(
        'freight.order.package', string='Freight Order Package')
