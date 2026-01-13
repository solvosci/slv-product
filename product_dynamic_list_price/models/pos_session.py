# © 2026 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import fields, models


class PosSession(models.Model):
    _inherit = "pos.session"

    def _process_pos_ui_product_product(self, products):
        super()._process_pos_ui_product_product(products)
        for product in products:
            product['list_price_2'] = self.env['product.product'].browse(product['id']).list_price_2
