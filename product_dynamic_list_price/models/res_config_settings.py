# © 2026 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    reference_pricelist_id = fields.Many2one(
        "product.pricelist",
        string="Reference Pricelist for Dynamic Sale Price",
        related="company_id.reference_pricelist_id",
        readonly=False,
        # required=True,
    )
