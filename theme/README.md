# Inline image text — Shopify section

A heading where small photo thumbnails sit inline between the words, on the text
baseline, wrapping with the text like any other word.

`sections/inline-image-text.liquid`

## Install

1. Shopify admin → **Online Store → Themes → ⋯ → Edit code**
2. Under **Sections**, click **Add a new section**, name it `inline-image-text`
3. Replace the generated file's contents with `sections/inline-image-text.liquid`
4. Save

Or with the Shopify CLI:

```bash
cp theme/sections/inline-image-text.liquid <your-theme>/sections/
shopify theme push --only sections/inline-image-text.liquid
```

Then in the theme editor: **Add section → Inline image text**. It ships with a
preset, so it appears already composed and you edit from there.

## How a merchant composes the line

The sentence is built from blocks, rendered in the order they appear in the
sidebar. Drag to reorder, and the line recomposes.

| Block | What it does |
| --- | --- |
| **Text** | A run of words. Supports inline bold, italic and links. |
| **Image** | One thumbnail, rendered inline at that point in the sentence. |

Up to 30 blocks, so roughly a dozen thumbnails in a sentence.

### Spacing between words and thumbnails

Each Image block owns the gap on both sides of itself (**Space on each side**,
default `0.18em`). Don't also type spaces around thumbnails in the Text blocks —
you'll get a double gap. Text blocks preserve any leading and trailing spaces you
type, so you can override this if you want asymmetric spacing.

### Sizes are relative, not fixed

Thumbnail **Size** is in `em`, so thumbnails scale with the heading. Set the font
size once per breakpoint and the thumbnails follow. Nothing needs a separate
mobile value.

### Vertical alignment

Thumbnails use `vertical-align: middle`, which is font-agnostic but sits slightly
low against some typefaces. The **Vertical nudge** setting (`-0.4em` to `0.4em`)
corrects it per thumbnail without touching code.

## Settings

**Layout** — heading tag (H1/H2/H3/P), alignment, max width, side padding
**Type** — font size per breakpoint, line height, letter spacing, weight, body-vs-heading font, uppercase
**Colors** — text, background, thumbnail placeholder
**Thumbnails** — hover lift on linked thumbnails
**Section padding** — top and bottom (scaled to 60% on mobile automatically)

**Per thumbnail** — image, shape (circle/rounded/square), corner radius, size,
height ratio, side spacing, vertical nudge, border width and color, link, alt text

## Accessibility

Leave **Alt text** empty for decorative thumbnails. They're then hidden from
screen readers so the sentence still reads as one clean line. A thumbnail that is
both decorative *and* linked is also removed from tab order — if a thumbnail links
somewhere that matters, give it alt text.

## Notes

- Theme-agnostic: no dependency on theme CSS, JS or snippets. All CSS is scoped
  to `#shopify-section-{{ section.id }}`, so two instances on one page can't
  collide.
- Built as an inline formatting context on purpose, **not** flexbox. Flex would
  make each text run an unbreakable item and stop the line wrapping around
  thumbnails.
- Images are served responsively (`srcset` 120–720px, `loading="lazy"`).
- `prefers-reduced-motion` disables the hover transition.
- Verified rendering at 1280px and 390px.
