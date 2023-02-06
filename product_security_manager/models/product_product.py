# © 2023 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)

from odoo import models, api, _


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def create(self, vals):
        self.product_tmpl_id.check_permission()
        return super().create(vals)

    def write(self, vals):
        fields_allowed = self.product_tmpl_id._fields_change_exceptions()
        fields_changed = list(vals.keys())
        changes_allowed = all(
            field in fields_allowed
            for field in fields_changed
        )
        if not changes_allowed:
            self.product_tmpl_id.check_permission(fields_changed=fields_changed)
        return super().write(vals)

    def unlink(self):
        self.product_tmpl_id.check_permission()
        return super().unlink()
