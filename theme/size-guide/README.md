# Size guide — superseded

This was a "Size guide" link under the size selector that opened the XS–XXL chart
in a modal, built on Horizon's `dialog.js`.

**It is no longer used.** The same chart now lives in the **Fit & sizes** row of
the Product info block (`theme/product-info/`), and the link under the size
selector scrolls to that row and opens it instead of opening a modal. Keeping both
would have shown the same table twice on every apparel product.

What replaced it:

| Was | Now |
| --- | --- |
| `snippets/size-guide-link.liquid` | `theme/product-info/snippets/size-guide-jump.liquid` |
| `snippets/size-guide-tables.liquid` | The **Size chart** setting on the Product info block |

The two old snippets are still present on the theme as orphans — nothing renders
them, and `themeFilesDelete` is blocked by the connector's safety policy, so
removing them is a manual step in Shopify admin (Edit code → Snippets → delete
`size-guide-link.liquid` and `size-guide-tables.liquid`). Leaving them does no
harm beyond clutter.

The sizing-system research behind the original build still stands and is worth
keeping: the catalogue runs **three** systems — XS–XXL (153 products), 28S–38L
denim (23), and One Size (3) — so a single chart cannot serve all of them. The
Product info block carries that logic forward: it hides **Fit & sizes** on One
Size products, and a per-product `custom.size_chart` metafield overrides the chart
for a category that needs different measurements, such as denim.
