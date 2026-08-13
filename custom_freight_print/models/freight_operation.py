from odoo import models, fields


class FreightOperation(models.Model):
       _inherit = 'freight.operation'
       etd_date = fields.Date(string='ETD')

       quick_search = fields.Char(
           compute='_compute_quick_search', search='_search_quick_search',
           help='Campo solo de búsqueda: al usarlo, busca simultáneamente en Nombre, OBL, MAWB No y Número de Contenedor.')

       def _compute_quick_search(self):
           for rec in self:
               rec.quick_search = False

       def _search_quick_search(self, operator, value):
           return ['|', '|', '|',
                   ('name', operator, value),
                   ('obl', operator, value),
                   ('mawb_no', operator, value),
                   ('container_number', operator, value)]