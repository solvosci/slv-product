# © 2021 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)

from odoo import models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def _name_search(self, name, args, operator="ilike", limit=None, name_get_uid=None):
        if len(name) < 5:
            return []
        product_ids = list(
            self.env["product.template"]._search(
            ['|', '|', '|',
            ("default_code", operator, name),
            ('product_variant_ids.default_code', operator, name),
            ('name', operator, name),
            ('barcode', operator, name)] + args,
            limit=limit,
            access_rights_uid=name_get_uid,
        ))
        return product_ids
