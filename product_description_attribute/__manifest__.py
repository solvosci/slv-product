# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)
{
    "name": "Product Description Attribute",
    "summary": """
        Add variant values in the product description if the attribute only has one value
        and if the attribute has the ‘include_variant_name’ field checked.
    """,
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "17.0.1.0.0",
    "category": "Product",
    "website": "https://github.com/solvosci/slv-product",
    "depends": ["product"],
    "data": [
        "views/product_attribute_views.xml",
    ],
    "installable": True,
}
