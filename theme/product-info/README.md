# Product info — Shopify product page

Collapsible product information below the product description: a composition
summary, three accordion rows with icons, a share button and a dark secure-payments
block.

```
blocks/product-info.liquid        the block: markup, styles, settings
blocks/variant-picker.liquid      one line added, to render the size guide link
snippets/pinfo-chevron.liquid     the chevron that rotates when a row opens
snippets/size-guide-jump.liquid   the "Size guide" link under the size selector
templates/product.json            the default product template, with the block added
```

Built for **Horizon 4.x** on `driphope.com`. Native `<details>`/`<summary>`, so the
accordions need no JavaScript and work closed-by-default with correct keyboard and
screen-reader behaviour. The only script is the share button.

## Install

The block is already in `templates/product.json`, so it appears on every product
using the default template — nothing to add in the theme editor.

To install by hand: add the two Liquid files, then add this block to
`sections.main.blocks["product-details"].blocks` and append its id to that same
object's `block_order` (last, so it sits under the description):

```json
"product_info_dripPI": {
  "type": "product-info",
  "settings": {},
  "blocks": {}
}
```

`settings` is intentionally empty — every value falls back to the schema default in
`blocks/product-info.liquid`, so defaults live in one place and the theme editor
still exposes them.

## Metafields

Create these on **Products** (Settings → Custom data → Products). All are
`multi_line_text_field`.

| Metafield | Fills | Empty behaviour |
| --- | --- | --- |
| `custom.composition` | The "Composition" summary and the top of the first accordion | Summary hidden |
| `custom.care_instructions` | The "Care" part of the first accordion | Care hidden |
| `custom.size_chart` | Optional. Replaces the size chart for that product only | Falls back to the block setting |

One item per line; each line renders as a bullet. If both `composition` and
`care_instructions` are empty, the whole "Composition & care" row is hidden rather
than rendering an empty accordion.

`custom.size_chart` uses the same pipe format as the theme-editor setting: first
line is the header row, columns separated by `|`.

```
Size|IT|Bust|Waist|Hips
XS|38|78–82|60–64|86–90
```

**The source data already exists.** Product descriptions imported from ARNE carry
`Fabric — 65% cotton 35% polyester` and `Care — Machine wash gentle 30 degree…`
lines, so the metafields can be backfilled from each product's own description
rather than typed by hand.

## Theme editor settings

Everything that is the same across products is a block setting, editable under the
**Product info** block:

| Group | Settings |
| --- | --- |
| Composition | Heading, row title, care subheading |
| Fit & sizes | Row title, intro text, **size chart**, measuring subheading and items, fit subheading and text |
| Shipping & returns | Row title, **shipping text** |
| Share | Show/hide, label, copied confirmation |
| Secure payments | Show/hide, title, text |
| Padding | Top, bottom, left, right |

The size chart and the "how to measure" list are textareas parsed on `|`, so they
are edited as plain text rather than HTML. A per-product `custom.size_chart`
metafield overrides the chart for that product, which is how a different product
category gets a different chart.

The shipping text reads "delivered in 2–4 business days", set by the merchant.
It is the same on every product and lives in the block setting, so changing the
window is one edit in the theme editor rather than a per-product change.

## Size guide link

A small "Size guide" link sits under the size selector. It scrolls to the
**Fit & sizes** row and opens it, rather than opening a separate modal, so the
chart exists in exactly one place.

It is a real `<a href="#SizeGuideTarget-{id}">`, so without JavaScript it still
jumps to the row; the script adds `open`, smooth scrolling and focus. The scroll
is instant under `prefers-reduced-motion`, and focus moves to the row's summary so
keyboard and screen reader users land there too, not just sighted ones.

The link and the row share one visibility rule, so they can never disagree: both
check the product's **Size** option and disappear on products with no sizes or a
single "One Size" value. That stops a backpack showing a bust/waist/hips chart.
Reverting that is one condition — drop `{%- if has_sizes -%}` around the
Fit & sizes row in `blocks/product-info.liquid`.

## Implementation notes

- Native `<details>`/`<summary>`; no JS, closed by default, and the chevron rotates
  via `.pinfo__row[open] .pinfo__chevron`. `prefers-reduced-motion` disables it.
- Borders use `color-mix(in srgb, currentColor …)` rather than named theme colors,
  so rows follow whatever palette the product page inherits with no tokens to keep
  in sync. The secure-payments block is the one exception: `#000` / `#fff`, as specified.
- The size chart scrolls horizontally on narrow screens instead of shrinking its type.
- The panel is indented to line up under the row label on desktop and flush left on
  mobile.
- The share button uses the Web Share API, falls back to the clipboard, then to a
  prompt. It binds by selector and marks bound buttons, so a section re-render
  (variant change) cannot double-bind or leave it dead.
- `<th scope="row">` on size cells, `scope="col"` on headers, `role="region"` with a
  label on the scroll container, and `:focus-visible` on each summary.

## Verification

`templates/product.json` was reproduced by hand and proven correct **before** any
upload: the reconstruction, emitted as header + pretty JSON + CRLF + trailing
newline, hashes to `842d895dd93de9f83fb7ac8349782a7d` — the live file's exact
checksum. The patch was then applied programmatically, with an assertion that a copy
of the result minus the new block equals the original leaf for leaf.

Note for future edits: these JSON templates are stored **verbatim** in that exact
form, not minified. An earlier revision of this project assumed minification, based
on `footer-group.json`; that assumption was wrong and is corrected here.

| File | md5 | Bytes |
| --- | --- | --- |
| `blocks/product-info.liquid` | `f34b08e96618cf71d374f3bd879e60ba` | 18820 |
| `snippets/pinfo-chevron.liquid` | `2b18630d81cb21f673e602bc89bd5906` | 441 |
| `templates/product.json` | `8b665b13cf564ef3464af4dac3053792` | 14679 |

All three read back from the theme and matched.

**Not visually verified.** The session's egress proxy returns 403 for the
storefront, so no rendered page was loaded. Checksums prove the stored bytes; they
do not prove the page renders.

Deployed to `DRIPHOPE (size-guide-2026-10-02)` (theme `154274562117`), unpublished,
alongside the size guide. Writes to the live theme and `themePublish` are both
blocked by the connector's safety policy.

## Overlap with the size guide

`snippets/size-guide-link.liquid` puts the same XS–XXL chart in a modal under the
size selector. The "Fit & sizes" accordion now carries that chart too, so the two
overlap on every apparel product. Pick one:

- **Keep the accordion**, drop the modal: remove the
  `{% render 'size-guide-link' %}` line from `blocks/variant-picker.liquid`.
- **Keep the modal**, drop the chart from the accordion: clear the **Size chart**
  setting on the Product info block.
