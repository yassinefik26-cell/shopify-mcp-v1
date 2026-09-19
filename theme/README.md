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

## Color

Color comes from the theme's own color scheme system, not from a private palette.
The section applies `class="color-{{ section.settings.color_scheme }}"` to its
wrapper — the convention Shopify documents for `color_scheme` settings — and the
heading uses `color: inherit`, so background and text color come from whichever
scheme the merchant picks. Change a scheme in **Theme settings → Colors** and this
section follows.

- **Color scheme** — picks from the theme's schemes. Default `scheme-1`; if a theme
  names its schemes differently, Shopify falls back to the first defined scheme
  rather than breaking.
- **Text color override** — optional, leave empty to use the scheme's text color.
- Thumbnail placeholders tint from `currentColor`, so they sit correctly on light
  and dark schemes with nothing to configure.

Per **Text** block there is also an optional color, for fading the closing words
the way the reference design does.

## How a merchant composes the line

The sentence is built from blocks, rendered in the order they appear in the
sidebar. Drag to reorder, and the line recomposes.

| Block | What it does |
| --- | --- |
| **Text** | A run of words. Supports inline bold, italic and links, plus an optional color. |
| **Image** | One thumbnail, rendered inline at that point in the sentence. |

Up to 30 blocks, so roughly a dozen thumbnails in a sentence.

## Proportions

Defaults are measured from the reference design rather than guessed. At its 60px
heading:

| | Reference | Default |
| --- | --- | --- |
| Upright oval | 1.17em × 1.66em | 1.2em wide, height ratio 1.4 (= 1.68em) |
| Landscape crop | 1.93em × 1.40em | 1.95em wide, height ratio 0.7 (= 1.37em) |
| Line height | 1.72 | 1.7 |
| Space beside a thumbnail | 0.25em | 0.24em |

**Shape** — *Ellipse / circle* becomes a true circle when Height ratio is 1, and an
upright oval above 1. *Rounded rectangle* and *Square* are also available, set per
thumbnail, so one line can mix upright ovals with wide landscape crops as the
reference does.

**Sizes are relative, not fixed.** Thumbnail width is in `em`, so thumbnails scale
with the heading. Set the font size once per breakpoint and the thumbnails follow —
no separate mobile sizing.

**Spacing.** Each Image block owns the gap on both sides of itself. Don't also type
spaces around thumbnails in the Text blocks — you'll get a double gap. Text blocks
preserve any leading and trailing spaces you type, if you want asymmetric spacing.

**Vertical alignment.** Thumbnails use `vertical-align: middle`, which measured
within 0.03em of the reference, so no nudge is needed by default. The **Vertical
nudge** setting corrects per thumbnail for typefaces that sit differently.

## Other settings

**Layout** — heading tag (H1/H2/H3/P), alignment, line balancing, max width, side padding
**Type** — font size per breakpoint, line height, letter spacing, weight, body-vs-heading font, uppercase
**Thumbnails** — hover lift on linked thumbnails
**Section padding** — top and bottom (scaled to 60% on mobile automatically)

**Per thumbnail** — image, shape, corner radius, width, height ratio, side spacing,
vertical nudge, border width and color, link, alt text

## Accessibility

Leave **Alt text** empty for decorative thumbnails. They're then hidden from screen
readers so the sentence reads as one clean line.

A thumbnail that is both decorative *and* linked is also removed from tab order.
That is correct for a decorative duplicate link, but it means **a thumbnail linking
somewhere that matters must have alt text**, or keyboard users can't reach it.

## Notes

- Built as an inline formatting context, **not** flexbox. Flex would make each text
  run an unbreakable item and stop the line wrapping around thumbnails.
- CSS is scoped to `#shopify-section-{{ section.id }}`, so two instances on one page
  can't collide. No dependency on theme CSS, JS or snippets beyond the scheme class.
- Images are served responsively (`srcset` 120–720px, `loading="lazy"`).
- `prefers-reduced-motion` disables the hover transition.
- Verified: schema JSON, every setting type, range step and preset value checked
  programmatically; rendered at 1900px, 1280px and 390px; scheme inheritance
  confirmed against a simulated light and dark theme scheme.
