from odoo import models, fields


class FreightOperation(models.Model):
       _inherit = 'freight.operation'
       etd_date = fields.Date(string='ETD')