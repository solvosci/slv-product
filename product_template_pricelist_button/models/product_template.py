# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)

from odoo import models
from odoo.osv import expression

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def open_pricelist_rules(self):
        action = super().open_pricelist_rules()
        domain = action["domain"]
        domain_aux = expression.OR([
            domain,
            [ ("categ_id", "parent_of", self.categ_id.id)]
        ])
        action["domain"] = domain_aux
        return action

    def _compute_item_count(self):
        super()._compute_item_count()
        for template in self:
            domain_aux = [
                '&',
                ('pricelist_id.active', '=', True),
                ('categ_id','parent_of',template.categ_id.id)
            ]
            template.pricelist_item_count += self.env['product.pricelist.item'].search_count(domain_aux)
