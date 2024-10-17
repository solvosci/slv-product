# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)

{
    "name": "Product pricelist item formula visibility",
    "summary": """
        Make the base and compute_price fields visible in the pricelist item tree view.
        """,
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "17.0.1.0.0",
    "category": "Product",
    "website": "https://github.com/solvosci/slv-product",
    "depends": ["product"],
    "data": [
        "views/product_pricelist_item_views.xml",
        "views/product_pricelist_views.xml",
    ],
    "installable": True,
}
