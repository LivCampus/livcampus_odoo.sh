# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class FreightOrderPackage(models.Model):
    _name = 'freight.order.package'
    _description = 'Freight Order Package'
    _rec_name = 'description'

    freight_operation_id = fields.Many2one(
        'freight.operation', string='Freight Operation')
    description = fields.Char(string='Description', required=True)
    package_id = fields.Many2one(
        'freight.package', string='Package', required=True)
    quantity = fields.Float('Quantity')
    operation_value_id = fields.Many2one(
        'freight.operation.value', string='Operation')
    volume = fields.Float(string='Volume(CBM)')
    gross_weight = fields.Float(string='Gross Weight(KG)')
    freight_order_id = fields.Many2one('freight.order', string='Freight Order')
    freight_route_id = fields.Many2one('freight.route', string='Freight Route')
    dangerous_goods = fields.Boolean(string='Dangerous Goods')
    class_number = fields.Char(string='Class Number')
    un_number = fields.Char(string='UN Number')
    packaging_group = fields.Char(string='Packaging Group')
    imdg_code = fields.Char(string='IMDG Code')
    flash_point = fields.Char(string='Flash Point')
    material_desc = fields.Text(string='Material Description')
    harmonize = fields.Char(string='Harmonize')
    temperature = fields.Char(string='Temperature')
    vgm = fields.Char(string='VGM')
    carrier_seal = fields.Char(string='Carrier Seal')
    shipper_seal = fields.Char(string='Shipper Seal')
    reference = fields.Char(string='Reference')
    item_ids = fields.One2many(
        'freight.order.package.item', 'freight_order_package_id', string='Items')
    freight_route_package_ids = fields.One2many(
        'freight.route.package', 'freight_package_id', string='Freight Routes')

    @api.model_create_multi
    def create(self, vals):
        values = super(FreightOrderPackage, self).create(vals)
        for record in values:
            if record.freight_operation_id and record.freight_operation_id.freight_route_ids:
                for route in record.freight_operation_id.freight_route_ids:
                    for package in values:
                        if not package.id in route.freight_packages_ids.ids:
                            route.freight_packages_ids = [
                                (0, 0, {'freight_package_id': package.id, 'route_id': route.id})]
        return values

    def unlink(self):
        for record in self:
            if record.freight_route_package_ids:
                for line in record.freight_route_package_ids:
                    line.write({'route_id': False})
        return super(FreightOrderPackage, self).unlink()
