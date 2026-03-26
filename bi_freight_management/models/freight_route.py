# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api

SELECTION_TYPE = [('pickup', 'Pickup'), ('on_carriage', 'On Carriage'), ('pre_carriage', 'Pre Carriage'),
                  ('delivery', 'Delivery'), ('to_warehouse', 'To Warehouse'), ('from_warehouse', 'From Warehouse')]


class FreightRoutePackage(models.Model):
    _name = 'freight.route.package'
    _description = 'Freight Route Package'

    route_id = fields.Many2one('freight.route', string='Route')
    freight_package_id = fields.Many2one(
        'freight.order.package', string='Packages')


class FreightRoute(models.Model):
    _name = 'freight.route'
    _description = 'Freight Route'
    _rec_name = 'route_operation'

    type = fields.Selection(SELECTION_TYPE, string='Type', required=True)
    route_operation = fields.Char('Route Operation')
    source = fields.Char('Source Location')
    destination = fields.Char('Destination Location')
    transport = fields.Selection(
        [('air', 'Air'), ('ocean', 'Ocean'), ('land', 'Land')], string='Transport', required=True)
    from_port_id = fields.Many2one('freight.port', string='From')
    to_port_id = fields.Many2one('freight.port', string='To')
    date = fields.Datetime(string='Date')
    cmr_rwb_pro = fields.Char(string='CMR/RWB#/Pro#')
    trucker_id = fields.Many2one('freight.trucker', string='Trucker')
    trucker_no = fields.Char(string='Trucker No')
    freight_operation_id = fields.Many2one(
        'freight.operation', string='Freight Operation')
    gateway_id = fields.Many2one('res.country', string='Gateway')
    mawb_no = fields.Char(string='MAWB No')
    airline_id = fields.Many2one('freight.airline', string='Airline')
    flight_no = fields.Char(string='Flight No')
    loading_port_id = fields.Many2one('freight.port', string='Loading Port')
    discharge_port_id = fields.Many2one(
        'freight.port', string='Discharge Port')
    shipping_line_id = fields.Many2one(
        'res.partner', string='Shipping Line')
    voyage_no = fields.Char(string='Voyage No')
    destination_id = fields.Many2one('res.country', string='Destination')
    vessel_id = fields.Many2one('freight.vessel', string='Vessel')
    obl = fields.Char(string='OBL')
    etd = fields.Date('ETD')
    eta = fields.Date('ETA')
    atd = fields.Date('ATD')
    ata = fields.Date('ATA')
    freight_route_package_ids = fields.One2many('freight.order.package', 'freight_route_id',
                                                string='Freight Orders Packages')
    freight_service_ids = fields.One2many(
        'freight.service', 'freight_route_id', string='Services')
    freight_packages_ids = fields.One2many(
        'freight.route.package', 'route_id', string='Packages')

    @api.onchange('type', 'transport', 'from_port_id', 'to_port_id', 'loading_port_id', 'discharge_port_id',
                  'gateway_id', 'destination_id')
    def onchange_transport(self):
        if not self._context.get('create_from_operation'):
            loopup = {k: v for k, v in SELECTION_TYPE}
            for rec in self:
                if rec.type:
                    rec.route_operation = loopup.get(rec.type)
                if rec.transport == 'air' and rec.gateway_id and rec.destination_id:
                    rec.source = rec.gateway_id.name
                    rec.destination = rec.destination_id.name
                if rec.transport == 'ocean' and rec.loading_port_id and rec.discharge_port_id:
                    rec.source = rec.loading_port_id.name
                    rec.destination = rec.discharge_port_id.name
                if rec.transport == 'land' and rec.from_port_id and rec.to_port_id:
                    rec.source = rec.from_port_id.name
                    rec.destination = rec.to_port_id.name
