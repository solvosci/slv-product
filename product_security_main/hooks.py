# # © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# # License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo.api import SUPERUSER_ID, Environment


def uninstall_hook(cr, registry):
    env = Environment(cr, SUPERUSER_ID, {})
    access_ids = [
        "product.access_product_template_manager",
        "product.access_product_product_manager",
        "stock.access_product_template_stock_manager",
        "stock.access_product_product_stock_manager",
        "mrp.access_product_template_mrp_manager",
        "mrp.access_product_product_mrp_manager",
        "sale.access_product_template_sale_manager",
        "sale.access_product_product_sale_manager",
        "purchase.access_product_template_purchase_manager",
        "purchase.access_product_product_purchase_manager",
        "account.access_product_template_account_manager",
        "account.access_product_product_account_manager",
    ]

    models = env["ir.model.access"].browse([])
    for xml_id in access_ids:
        models |= env.ref(xml_id, raise_if_not_found=False)
    if models:
        models.write({"perm_create": True})
