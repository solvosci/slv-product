# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models

class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    extra = fields.Float(string="Extra", default=0.0)