# © 2023 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)

from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = "product.product"

    other_references = fields.Char()

    @api.model
    def _name_search(self, name, args, operator="ilike", limit=None, name_get_uid=None):
        res = super(ProductProduct, self)._name_search(
            name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid
        )
        res_ids = list(res)
        product_ids = list(
            self._search([('other_references', operator, name)],
            limit=limit,
            access_rights_uid=name_get_uid
            )
        )
        res_ids.extend(product_ids)

        return list(set(res_ids))
