# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "Product Default Route By Category",
    "summary": """
        Automatically links product categories with their default stock routes and keeps them synchronized when creating or updating products.
        When creating or updating a product:
            - If a route is assigned that corresponds to a category’s default route, the product category is automatically set.
            - Changing the product category updates the routes to match the new category’s default route.
            - Routes not linked to any category are preserved.
    """,
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "15.0.1.0.0",
    "category": "Product",
    "website": "https://github.com/solvosci/slv-product",
    "depends": ["stock"],
    "data": [
        "views/product_category_views.xml"
    ],
    "installable": True,
}
