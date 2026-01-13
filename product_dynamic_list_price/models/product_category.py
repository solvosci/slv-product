# © 2026 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import _, models
from odoo.exceptions import UserError


class ProductCategory(models.Model):
    _inherit = "product.category"

    def action_recalculate_list_price_2(self):
        max_products_count = int(
            self.env["ir.config_parameter"].sudo().get_param(
                "product_dynamic_list_price.recalculate_manual_max_products",
                100
            )
        )
        product_count = sum(self.mapped("product_count"))
        if product_count > max_products_count:
            raise UserError(_(
                "You cannot recalculate RRP prices for more than %d product(s),"
                " and %d were selected.\n\n"
                "Please select less categories and/or categories with less products,"
                " or ask an Administrator for increasing current max. products thereshold",
                max_products_count,
                product_count,
            ))
        product_ids = self.env["product.template"].search([
            ("categ_id", "child_of", self.ids)
        ])
        product_ids._recalculate_list_price_2()
        return True
