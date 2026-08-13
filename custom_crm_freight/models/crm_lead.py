from odoo import models

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def action_crm_to_freight_new(self):
        if not self.partner_id:
            return self.env["ir.actions.actions"]._for_xml_id("sale_crm.crm_quotation_partner_action")
        
        try:
            view_id = self.env.ref('bi_freight_management.freight_booking_view_form').id
        except ValueError:
            view_id = False
            
        return {
            'name': 'New Booking',
            'type': 'ir.actions.act_window',
            'res_model': 'freight.booking',
            'view_mode': 'form',
            'views': [[view_id, 'form']] if view_id else False,
            'target': 'current',
            'context': {
                'default_shipper_id': self.partner_id.id,
                'default_company_id': self.company_id.id or self.env.company.id,
                'default_user_id': self.user_id.id if self.user_id else False,
            }
        }

    def action_view_freight_bookings(self):
        self.ensure_one()
        return {
            'name': 'Bookings',
            'type': 'ir.actions.act_window',
            'res_model': 'freight.booking',
            'view_mode': 'list,form',
            'target': 'current',
            'domain': [('shipper_id', '=', self.partner_id.id)] if self.partner_id else [],
            'context': {
                'default_shipper_id': self.partner_id.id if self.partner_id else False,
            }
        }
