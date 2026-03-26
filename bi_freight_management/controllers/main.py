# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import base64
from odoo import http
from odoo.http import request


class FreightTrack(http.Controller):

    @http.route('/booking/create/', auth='public', website=True, methods=['POST'], csrf=False)
    def booking_create(self, **kw):
        massage = 'Opps Some value is Missing! Please Fill first'
        create = False
        vals = {'operation': kw.get('operation'), 'direction': kw.get('direction'),
                'transport': kw.get('transport'), 'shipper_id': kw.get('shipper_id'),
                'consignee_id': kw.get('consignee_id'), 'barcode': kw.get('barcode'),
                'dangerous_goods': True if kw.get('dangerous_goods') else False,
                'agent_id': kw.get('agent_id'), 'user_id': kw.get('user_id'),
                'freight_pc_id': kw.get('freight_pc_id'), 'freight_other_pc_id': kw.get('freight_other_pc_id'),
                'move_type_id': kw.get('move_type_id'), 'tracking_no': kw.get('tracking_no'),
                'incoterm_id': kw.get('incoterm_id')}

        if vals['transport'] == 'air':
            if kw.get('gateway_id') and kw.get('destination_id'):
                vals.update({'gateway_id': kw.get('gateway_id'), 'destination_id': kw.get('destination_id'),
                             'date': kw.get('air_date') or False, 'mawb_no': kw.get('mawb_no'),
                             'airline_id': kw.get('airline_id'), 'flight_no': kw.get('flight_no')})
            else:
                return request.render('bi_freight_management.booking_create_massage',
                                      {'massage': massage, 'create': create})

        if vals['transport'] == 'ocean':
            if kw.get('loading_port_id') and kw.get('discharge_port_id') and kw.get('ocean_shipment_type'):
                vals.update(
                    {'ocean_shipment_type': kw.get('ocean_shipment_type'), 'loading_port_id': kw.get('loading_port_id'),
                     'discharge_port_id': kw.get('discharge_port_id'),
                     'shipping_line_id': kw.get('shipping_line_id'), 'voyage_no': kw.get('voyage_no'),
                     'vessel_id': kw.get('vessel_id'),
                     'date': kw.get('ocean_date') or False, 'obl': kw.get('obl')})
            else:
                return request.render('bi_freight_management.booking_create_massage',
                                      {'massage': massage, 'create': create})

        if vals['transport'] == 'land':
            if kw.get('from_port_id') and kw.get('to_port_id') and kw.get('inland_shipment_type'):
                vals.update(
                    {'inland_shipment_type': kw.get('inland_shipment_type'), 'from_port_id': kw.get('from_port_id'),
                     'to_port_id': kw.get('to_port_id'),
                     'date': kw.get('land_date') or False, 'cmr_rwb_pro': kw.get('cmr_rwb_pro'),
                     'trucker_id': kw.get('trucker_id'), 'trucker_no': kw.get('trucker_no')})
            else:
                return request.render('bi_freight_management.booking_create_massage',
                                      {'massage': massage, 'create': create})

        record = request.env['freight.booking'].sudo().create(vals)
        if record:
            file = request.httprequest.files.getlist('file')
            if file:
                for i in range(len(file)):
                    record.write({'file': base64.b64encode(file[i].read()), 'file_name': file[i].filename})
            create = True
            massage = f'Your Booking Request is successfully Generated \n Your Booking ID is {record.name}'
        return request.render('bi_freight_management.booking_create_massage', {'massage': massage, 'create': create})

    @http.route('/booking/', auth='user', website=True)
    def booking(self, **kw):
        if request.env.user.has_group('base.group_system'):
            bookings = request.env['freight.booking'].sudo().search([])
        else:
            bookings = request.env['freight.booking'].sudo().search([('create_uid', '=', request.env.user.id)])
        partners = request.env['res.partner'].sudo().search([])
        countries = request.env['res.country'].sudo().search([])
        airlines = request.env['freight.airline'].sudo().search([])
        ports = request.env['freight.port'].sudo().search([])
        vessels = request.env['freight.vessel'].sudo().search([])
        truckers = request.env['freight.trucker'].sudo().search([])
        move_types = request.env['freight.move.type'].sudo().search([])
        users = request.env['res.users'].sudo().search([])
        incoterms = request.env['freight.incoterms'].sudo().search([])
        freight_pcs = request.env['freight.pc'].sudo().search([])
        other_pcs = request.env['freight.other.pc'].sudo().search([])
        return request.render('bi_freight_management.booking', {
            'partners': partners, 'countries': countries,
            'airlines': airlines, 'ports': ports, 'vessels': vessels,
            'truckers': truckers, 'move_types': move_types,
            'users': users, 'incoterms': incoterms, 'freight_pcs':
                freight_pcs, 'other_pcs': other_pcs, 'bookings': bookings})

    @http.route('/track/', auth='public', website=True , sitemap=True)
    def track(self, **kw):
        return request.render('bi_freight_management.track_shipment')

    @http.route('/track/search/', auth='public', website=True, methods=['POST'], csrf=False)
    def track_search(self, **kw):
        track_name = False
        operation = request.env['freight.booking']
        if kw.get('name'):
            track_name = kw.get('name').upper().replace(" ", "")
        operation = operation.sudo().search(
            [('name', '=', track_name)], limit=1)
        if operation:
            if operation.freight_operation_id:
                operation = operation.freight_operation_id
                return request.render('bi_freight_management.track_details', {'track_name': track_name, 'house': operation,
                                                                            'track_details': operation.freight_tracking_ids})
            else:
                return request.render('bi_freight_management.track_details', {'track_name': track_name})
        if not operation:
            operation = request.env['freight.operation']
            operation = operation.sudo().search(
                [('name', '=', track_name)], limit=1)
        if not operation:
            return request.render('bi_freight_management.track_details', {'track_name': track_name})
        return request.render('bi_freight_management.track_details', {'track_name': track_name, 'house': operation,
                                                                      'track_details': operation.freight_tracking_ids})
