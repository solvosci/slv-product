If a product already exists with a category and a specific route, and the user:

- Changes the category (triggering an automatic route update),
- Then manually reverts the route back to its original value, the product’s category does not update correctly because Odoo’s write or onchange logic sees no change in the route.
