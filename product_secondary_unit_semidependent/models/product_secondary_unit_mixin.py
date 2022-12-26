# © 2022 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import api, models


class ProductSecondaryUnitMixin(models.AbstractModel):
    _inherit = "product.secondary.unit.mixin"

    @api.model
    def _get_secondary_uom_qty_depends(self):
        return super(ProductSecondaryUnitMixin, self)._get_secondary_uom_qty_depends()

    @api.depends(lambda x: x._get_secondary_uom_qty_depends())
    def _compute_secondary_uom_qty(self):
        for line in self:
            if not line.secondary_uom_id.dependency_type == "semidependent":
                super(ProductSecondaryUnitMixin, self)._compute_secondary_uom_qty()
