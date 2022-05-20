# © 2022 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    root_categ_id = fields.Many2one(related="categ_id.root_id", store=True)
