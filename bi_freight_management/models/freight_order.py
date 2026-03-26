# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class FreightOrder(models.Model):
    _name = 'freight.order'
    _description = 'Freight Order'

    freight_operation_id = fields.Many2one('freight.operation', string='Freight Operation')
    description = fields.Char(string='Description', required=True)
    package_id = fields.Many2one('freight.package', string='Package', required=True)
    quantity = fields.Float('Quantity')
    operation_value_id = fields.Many2one('freight.operation.value', string='Operation')
    volume = fields.Float(string='Volume(CBM)')
    gross_weight = fields.Float(string='Gross Weight(KG)')
    freight_order_package_id = fields.Many2one('freight.order.package', string='Freight Order Package')
