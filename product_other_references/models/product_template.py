# © 2023 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)

from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    other_references = fields.Char(
        'Internal Reference', compute='_compute_other_references',
        inverse='_set_other_references')

    def _compute_other_references(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.other_references = template.product_variant_ids.other_references
        for template in (self - unique_variants):
            template.other_references = False

    def _set_other_references(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.other_references = template.other_references

    @api.model
    def _name_search(self, name, args, operator="ilike", limit=None, name_get_uid=None):
        product_template_extra_domain = ('product_variant_ids.other_references', operator, name)
        return super(ProductTemplate, self.with_context(
            product_template_extra_domain=product_template_extra_domain))._name_search(
                name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)
