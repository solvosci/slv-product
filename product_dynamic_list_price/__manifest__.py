# © 2026 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "Product Dynamic List Price",
    "summary": """
        Adds support for dynamic product sale pricing based on a reference pricelist.
    """,
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "17.0.1.0.0",
    "category": "Product",
    "website": "https://github.com/solvosci/slv-product",
    "depends": ["product", "point_of_sale"],
    "data": [
        "data/product_product.xml",
        "views/product_template_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "product_dynamic_list_price/static/src/js/product_price_patch.js",
        ],
    },
    "installable": True,
}
