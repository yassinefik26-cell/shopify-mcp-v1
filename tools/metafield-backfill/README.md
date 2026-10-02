# Metafield backfill — composition & care

Fills `custom.composition` and `custom.care_instructions` on every product from
that product's own description, so the Product info block has data to show
without anyone typing it twice.

The ARNE-sourced descriptions carry the data in a fixed shape:

```html
<li><strong>Fabric</strong> — 65% cotton 35% polyester</li>
<li><strong>Care</strong> — Machine wash gentle 30 degree. Wash with ...</li>
```

## Files

| File | What it is |
| --- | --- |
| `all.tsv` | `productId <tab> fabric <tab> careKey` for every product that has the data |
| `all.none` | Product ids whose description carries no Fabric/Care at all |
| `care.py` | The 16 distinct Care strings, verbatim, keyed `C1`–`C16` |
| `gen.py` | Expands the above into `productUpdate` payloads |

Care text is deduplicated because only 16 distinct strings cover all 161 products.
Fabric is not — there are 52 distinct values.

## Transformation

Both fields are **verbatim from the description**, with one change: each
sentence becomes its own line, so the block renders one bullet per instruction.

```
Machine wash gentle 30 degree. Wash with similar colours only. Do not bleach.
```
becomes
```
Machine wash gentle 30 degree
Wash with similar colours only
Do not bleach
```

Nothing is reworded. ARNE's phrasing ("30 degree", "Exclusive of trims",
"Do not tumble. Dry iron on low temperature.") is preserved as written, including
where it reads awkwardly, because rewriting 161 products' care text would be
inventing product data rather than migrating it.

## Coverage

| | Products |
| --- | --- |
| Backfilled | 161 |
| No source data in the description | 18 |
| Total | 179 |

The 18 are hoodies and sweatshirts whose descriptions end at `<strong>Fit</strong>`
with no Fabric or Care list. They were left untouched rather than guessed; the
Product info block hides its "Composition & care" row on those products
automatically. Their ids are in `all.none`.

## Verification

After the writes, every product was read back:

- 161 products have both metafields, 18 have neither, totalling 179.
- The 18 nulls are **exactly** the ids in `all.none` — verified by diff, not by eye.
- Values spot-checked against their source descriptions on a hoodie, a jeans and
  a windbreaker, covering the single-value, `Exclusive of trims` and multi-part
  (`Jersey: … Woven: … Lining: …`) shapes.

Every `productUpdate` returned `userErrors: []`.
