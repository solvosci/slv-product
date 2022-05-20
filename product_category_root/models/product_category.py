# © 2022 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import api, fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    root_id = fields.Many2one(
        comodel_name="product.category",
        compute="_compute_root_id",
        readonly=True,
        store=True,
        string="Root Category",
        help="Indicates the root category for this category,"
        " or the category itself if has no parents",
    )

    @api.depends("parent_id")
    def _compute_root_id(self):
        # TODO maybe a create/write update should be more appropiated,
        #      since this method can be change more than this category
        for category in self:
            category_root_id = category._get_root()
            category._update_root(category_root_id)
            # Alternative children categories update (poor performance,
            #  since we already know the final value)
            # category.root_id = category_root_id
            # category.child_id._compute_root_id()

    def _get_root(self):
        parent = self
        while True:
            if parent.parent_id:
                parent = parent.parent_id
            else:
                return parent

    def _update_root(self, category_root_id):
        for category in self:
            category.root_id = category_root_id
            category.child_id._update_root(category_root_id)
