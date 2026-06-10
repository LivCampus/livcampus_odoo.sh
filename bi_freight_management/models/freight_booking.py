# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, _, api
from odoo.exceptions import ValidationError


class FreightBooking(models.Model):
    _name = 'freight.booking'
    _description = 'Freight Booking'

    name = fields.Char(string='Name', required=True,
                       readonly=True, default=lambda self: _('New'))
    operation = fields.Selection(
        [('house', 'House'), ('direct', 'Direct'), ('master', 'Master')], string='Operation Type', copy=False,
        required=True)
    stage = fields.Selection(
        [('created', 'Created'), ('draft', 'Draft'), ('validate', 'Validate'), ('convert', 'Convert')], string='Stage',
        default='created', copy=False)
    direction = fields.Selection(
        [('import', 'Import'), ('export', 'Export')], string='Direction', required=True)
    transport = fields.Selection(
        [('air', 'Air'), ('ocean', 'Ocean'), ('land', 'Land')], string='Transport', required=True)
    ocean_shipment_type = fields.Selection(
        [('fcl', 'FCL'), ('lcl', 'LCL')], string='Ocean Shipment Type')
    inland_shipment_type = fields.Selection(
        [('ftl', 'FTL'), ('ltl', 'LTL')], string='Inland Shipment Type')
    shipper_id = fields.Many2one(
        'res.partner', string='Shipper', required=True)
    consignee_id = fields.Many2one(
        'res.partner', string='Consignee', required=True)
    gateway_id = fields.Many2one('res.country', string='Gateway')
    destination_id = fields.Many2one('res.country', string='Destination')
    mawb_no = fields.Char(string='MAWB No')
    airline_id = fields.Many2one('freight.airline', string='Airline')
    flight_no = fields.Char(string='Flight No')
    date = fields.Date(string='ETA')
    dangerous_goods = fields.Boolean(string='Dangerous Goods')
    file = fields.Binary('File', attachment=True)
    file_name = fields.Char('File Name')
    move_type_id = fields.Many2one('freight.move.type', string='Move Type')
    incoterm_id = fields.Many2one('freight.incoterms', string='Incoterm')
    tracking_no = fields.Char(string='Tracking Number')
    user_id = fields.Many2one('res.users', string='User')
    agent_id = fields.Many2one('res.partner', string='Agent')
    note = fields.Text(string='Notes')
    barcode = fields.Char(string='Barcode')
    freight_pc_id = fields.Many2one('freight.pc', string='Freight PC')
    freight_other_pc_id = fields.Many2one(
        'freight.other.pc', string='Other PC')
    loading_port_id = fields.Many2one('freight.port', string='Loading Port')
    discharge_port_id = fields.Many2one(
        'freight.port', string='Discharge Port')
    shipping_line_id = fields.Many2one(
        'res.partner', string='Shipping Line')
    voyage_no = fields.Char(string='Voyage No')
    vessel_id = fields.Many2one('freight.vessel', string='Vessel')
    obl = fields.Char(string='MBL')
    cmr_rwb_pro = fields.Char(string='CMR/RWB#/Pro#')
    from_port_id = fields.Many2one('freight.port', string='From')
    to_port_id = fields.Many2one('freight.port', string='To')
    trucker_id = fields.Many2one('freight.trucker', string='Trucker')
    trucker_no = fields.Char(string='Trucker No')
    freight_operation_id = fields.Many2one('freight.operation', string='Freight Operation')

    @api.model_create_multi
    def create(self, vals):
        for value in vals:
            if value.get('name', _('New')) == _('New'):
                value['name'] = self.env['ir.sequence'].next_by_code(
                    'freight.booking') or _('New')
        return super(FreightBooking, self).create(vals)

    def action_convert_shipment(self):
        if self.stage == 'convert':
            raise ValidationError(_("Already you are in Converted"))
        operation = self.env['freight.operation'].create({
            'stage': 'draft',
            'direction': self.direction,
            'transport': self.transport,
            'type': self.operation if self.operation else 'house',
            'ocean_shipment_type': self.ocean_shipment_type if self.ocean_shipment_type else False,
            'inland_shipment_type': self.inland_shipment_type if self.inland_shipment_type else False,
            'shipper_id': self.shipper_id.id,
            'consignee_id': self.consignee_id.id,
            'mawb_no': self.mawb_no if self.mawb_no else False,
            'gateway_id': self.gateway_id.id if self.gateway_id else False,
            'destination_id': self.destination_id.id if self.destination_id else False,
            'airline_id': self.airline_id.id if self.airline_id else False,
            'flight_no': self.flight_no,
            'date': self.date,
            'dangerous_goods': self.dangerous_goods,
            'move_type_id': self.move_type_id.id if self.move_type_id else False,
            'incoterm_id': self.incoterm_id.id if self.incoterm_id else False,
            'tracking_no': self.tracking_no,
            'user_id': self.user_id.id if self.user_id else False,
            'agent_id': self.agent_id.id if self.agent_id else False,
            'note': self.note,
            'barcode': self.barcode,
            'freight_pc_id': self.freight_pc_id.id if self.freight_pc_id else False,
            'freight_other_pc_id': self.freight_other_pc_id.id if self.freight_other_pc_id else False,
            'loading_port_id': self.loading_port_id.id if self.loading_port_id else False,
            'discharge_port_id': self.discharge_port_id.id if self.discharge_port_id else False,
            'shipping_line_id': self.shipping_line_id.id if self.shipping_line_id else False,
            'voyage_no': self.voyage_no,
            'vessel_id': self.vessel_id.id if self.vessel_id else False,
            'obl': self.obl,
            'cmr_rwb_pro': self.cmr_rwb_pro,
            'from_port_id': self.from_port_id.id if self.from_port_id else False,
            'to_port_id': self.to_port_id.id if self.to_port_id else False,
            'trucker_id': self.trucker_id.id if self.trucker_id else False,
            'trucker_no': self.trucker_no,
            'is_booking': True,
        })
        if operation:
            self.write({'stage': 'convert', 'freight_operation_id': operation.id})
        return True

    def action_open_shipment(self):
        self.ensure_one()
        if self.freight_operation_id:
            return {
                'name': _("Freight Operation"),
                'view_mode': 'form',
                'views': [[False, 'form']],
                'res_id': self.freight_operation_id.id,
                'res_model': 'freight.operation',
                'type': 'ir.actions.act_window',
                'context': self._context,
            }
