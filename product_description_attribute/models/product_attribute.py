# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)

from odoo import models, fields

class ProductAtribbute(models.Model):
    _inherit = 'product.attribute'

    include_variant_name = fields.Boolean()
