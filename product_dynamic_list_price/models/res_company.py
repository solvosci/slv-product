# © 2026 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    reference_pricelist_id = fields.Many2one(
        "product.pricelist",
        string="Reference Pricelist for Dynamic Sale Price",
    )
