Adds support for dynamic product sale pricing based on a reference pricelist.

This price can be used e.g. at Point of Sale as a replacement of standard list
price.

This price is recalculated at a cron that could be executed with caution (e.g.
once a day), depending on the amount of products involved. Such prices can be
manually recalculated for a set of products and/or categories. In order to
prevent database locks a maximum number of products can be updated at a time
(cron is not limited by this). That threshold can be updated with the system
parameter `product_dynamic_list_price.recalculate_manual_max_products`, set to
`100` by default.

Due to this calculation system, once installed it's recommended to properly
configure and initialize prices; otherwise will be set to `0,00`:

* Set the pricelist for dynamic price.
* Execute for the first time price update cron, or recalculate for the set of
  initial products, executing "Recalculate RRP" action.
