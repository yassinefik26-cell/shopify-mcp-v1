# Size guide — Shopify product page

A "Size guide" link under the size selector that opens the shared size chart in a
modal. One chart definition, shared by every product.

```
snippets/size-guide-tables.liquid   the chart data — single source of truth
snippets/size-guide-link.liquid     trigger + modal + styling
blocks/variant-picker.liquid        one line added to render the link
```

Built for **Horizon 4.x** on `driphope.com`. Reuses the theme's own modal system
(`assets/dialog.js`, `snippets/dialog-styles.liquid`), so it needs no app and adds
no third-party JavaScript.

## Install

Shopify admin → **Online Store → Themes → ⋯ → Edit code**, then **in this order**:

1. **Snippets → Add a new snippet**, name it `size-guide-tables`, paste
   `snippets/size-guide-tables.liquid`, save.
2. **Snippets → Add a new snippet**, name it `size-guide-link`, paste
   `snippets/size-guide-link.liquid`, save.
3. Open **Blocks → `variant-picker.liquid`** and add one line directly after the
   existing `variant-main-picker` render, inside the same `unless` block:

   ```liquid
   {% unless product_resource == blank %}
     {% render 'variant-main-picker', product_resource: product_resource, section: section, product: product %}
     {% render 'size-guide-link', product_resource: product_resource %}
   {% endunless %}
   ```

The order matters. Step 3 before steps 1–2 prints
`Liquid error: Could not find asset snippets/size-guide-link.liquid` on every
product page until the snippets exist.

Nothing to configure in the theme editor — the link appears on every product that
needs one.

## Three sizing systems

The link reads each product's own **Size** option values and picks the matching
chart. It renders nothing where a size guide would not apply, so it is safe to
render unconditionally.

| Size values | Products | Result |
| --- | --- | --- |
| `XS`–`XXL` | 153 — hoodies, sweatshirts, tees, jackets, coats, windbreakers, boxers | Apparel chart |
| `28S`–`38L` | 23 jeans | Denim chart |
| `One Size` | 3 backpacks | No link rendered |

Detection is by content, not product type: any digit in the size values means
denim, `one size` means no guide, anything else is the letter chart. Add a product
in a new category and it is covered automatically.

## Editing the chart

Everything measurable lives in `snippets/size-guide-tables.liquid`. Edit a row
there and every product page updates. No per-product duplication, no metafields.

### Apparel chart

Body measurements in centimetres, as supplied by the merchant.

| Size | EU | Chest | Waist | Hips |
| --- | --- | --- | --- | --- |
| XS | 38 | 78–82 | 60–64 | 86–90 |
| S | 40 | 82–86 | 64–68 | 90–94 |
| M | 42 | 86–90 | 68–72 | 94–98 |
| L | 44 | 90–96 | 72–78 | 98–104 |
| XL | 46 | 96–102 | 78–84 | 104–110 |
| XXL | 48 | 102–108 | 84–90 | 110–116 |

### Denim chart

The size code **is** the waist in inches, so the only derived column is the
centimetre conversion (`in × 2.54`, rounded):

| Size | Waist (in) | Waist (cm) |
| --- | --- | --- |
| 28 | 28" | 71 |
| 30 | 30" | 76 |
| 32 | 32" | 81 |
| 34 | 34" | 86 |
| 36 | 36" | 91 |
| 38 | 38" | 97 |

**Deliberately missing: inseam lengths and hip ranges.** `S`/`R`/`L` are explained
in words (Short / Regular / Long) rather than given as numbers, because the actual
inseam is a brand decision, not something derivable from the size code. Publishing
a guessed inseam would mislead customers more than omitting it. Supply the real
figures and add a column.

## Implementation notes

- The link is a **sibling after** the variant picker, not inside it. The Size
  fieldset sits inside a `<form>`; nesting a modal there risks interfering with
  `variant-picker.js` and with form submission.
- Colors come from `currentColor` and `color-mix()` rather than named theme
  variables, so the chart follows whatever palette the modal inherits, in light
  and dark, with no color tokens to keep in sync.
- The chart scrolls horizontally on narrow screens instead of shrinking its type,
  with the size column pinned via `position: sticky` so rows stay readable.
- Digit detection uses `'0,1,2,...' | split: ','`. An earlier revision used
  `split: ''` to get characters — if that returns the whole string rather than
  single characters, every jeans product silently gets the **apparel** chart. The
  comma form removes the assumption.
- `<th scope="row">` on the size cell and `scope="col"` on headers, `role="region"`
  with a label on the scroll container, and a real `<dialog>` for focus handling.
- Heading text is a literal, not a `t:` key. `| t` has no fallback for a missing
  key, so an absent translation would render
  `Translation missing: en.products.product.size_guide` on the storefront.

## Verification

`blocks/variant-picker.liquid` was reproduced byte-for-byte and its md5 confirmed
against the live theme (`b84d8a66a846fd093d87037ddbde770a`, 5207 bytes) *before*
editing, then the patch asserted to change exactly one line in exactly one place.
After upload, all three stored checksums matched these files exactly:

| File | md5 | Bytes |
| --- | --- | --- |
| `size-guide-tables.liquid` | `74da3f7958fa2bcc77ad76259d20925e` | 3485 |
| `size-guide-link.liquid` | `dd20cb4a29b8f29e9265ca11a0b3bd1c` | 6347 |
| `variant-picker.liquid` | `4b1c031123a8a3232d755afa488ac2e6` | 5277 |

**Not visually verified.** The session's egress proxy returns 403 for the
storefront, so no rendered page was ever loaded. Checksums prove the right bytes
are stored; they do not prove the page renders.

Deployed to `DRIPHOPE (size-guide-2026-10-02)` (theme `154274562117`), unpublished.
Writes to the live theme and `themePublish` are both blocked by the connector's
safety policy, so publishing is a manual step in Shopify admin.
