# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3.0 (https://www.gnu.org/licenses/agpl-3.0.html)

from odoo import models
from odoo.osv import expression


class ProductProduct(models.Model):
    _inherit = "product.product"

    def open_pricelist_rules(self):
        action = super().open_pricelist_rules()
        domain = action["domain"]
        domain_aux = expression.OR([
            domain,
            [ ("categ_id", "parent_of", self.categ_id.id)]
        ])
        action["domain"] = domain_aux
        # Default tree view has editable flag, we prefer form here for new & edit
        action["views"] = [
            (
                self.env.ref("product_template_pricelist_button.product_pricelist_item_tree_view_from_product_no_edit").id,
                "tree",
            ),
            (
                self.env.ref("product.product_pricelist_item_form_view").id,
                "form",
            ),
        ]
        return action

    def _compute_variant_item_count(self):
        super()._compute_variant_item_count()
        rule_obj = self.env["product.pricelist.item"]
        for product in self:
            domain_aux = [
                ("pricelist_id.active", "=", True),
                ("categ_id", "parent_of", product.categ_id.id)
            ]
            product.pricelist_item_count += rule_obj.search_count(domain_aux)
