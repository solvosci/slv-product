# © 2022 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import fields, models


class ProductSecondaryUnit(models.Model):
    _inherit = "product.secondary.unit"
    _description = "Product Secondary Unit"

    dependency_type = fields.Selection(
        selection=[
            ("dependent", "Dependent"),
            ("semidependent", "Semidependent"),
            ("independent", "Independent"),
        ],
    )

    def name_get(self):
        result = []
        for unit in self:
            result.append((unit.id, unit.name))
        return result
