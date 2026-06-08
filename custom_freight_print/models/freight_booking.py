from odoo import models, fields

class FreightBooking(models.Model):
    _inherit = 'freight.booking'

    commodity = fields.Char(string='Commodity')

    intructions_hbl  = fields.Char(string='Instruction for HBL', help='HBL is must with emission at destination')

    mbl_destination = fields.Char(string='MBL must be SWB or with insuance at destination')

    def action_button_printreport_freight(self):
        return self.env.ref('custom_freight_print.action_report_freight_booking').report_action(self)
