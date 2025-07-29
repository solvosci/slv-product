# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)

from odoo import models


class ProductTemplateAttributeValue(models.Model):
    _inherit = 'product.template.attribute.value'

    def _get_combination_name(self):
        super(ProductTemplateAttributeValue, self)._get_combination_name()
        """Exclude values from single value lines or from no_variant attributes."""
        ptavs = self._without_no_variant_attributes().with_prefetch(self._prefetch_ids)
        return ", ".join([ptav.name for ptav in ptavs.filtered(lambda x:x.product_attribute_value_id.attribute_id.include_variant_name)])
