# © 2026 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import api, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        # Restrict searches to at least 5 characters
        if len(name) < 5:
            return []
        return super().name_search(name=name, args=args, operator=operator, limit=limit)
