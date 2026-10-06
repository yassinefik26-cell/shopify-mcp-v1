# DRIPHOPE logo

## Current mark — Drop D

A solid geometric D whose counter is a teardrop. The pun lives in the negative
space, so nothing is stuck on top of the letterform, and the mark works in a
single ink.

    M48 40 H120 A88 88 0 0 1 120 216 H48 Z
    M126 71 C108 104 82 124 82 146 A44 44 0 1 0 170 146 C170 124 144 104 126 71 Z

on a 256x256 grid, `fill-rule="evenodd"`. Clearances around the counter are
34 left, 36 right, 31 top, 26 bottom — close enough to even that the ring reads
as one weight, which is what holds the mark together when it is scaled down.

Reversed (white on black) the counter becomes a positive black drop, so the
app icon is not merely an inverted copy.

### Files

| file | use |
|---|---|
| `driphope-mark-black.svg` | on light |
| `driphope-mark-white.svg` | on dark |
| `driphope-mark-currentcolor.svg` | inline in Liquid/HTML, inherits text colour |
| `driphope-appicon.svg` | black squircle, white mark |
| `png/driphope-mark-{black,white}-512.png` | raster, transparent background |
| `png/driphope-appicon-{512,192,180,32,16}.png` | favicon / app icon cuts |
| `png/driphope-lockup-{black,white}.png` | horizontal lockup, 1558x280 |

Regenerate the PNGs with `tools/logo-render/` — never by hand, and never by
scaling one cut to another (see that README on optical sizing).

## Lockup

Mark plus DRIPHOPE in Archivo 800, -0.025em tracking. Proportions follow the
approved artboard (mark box : wordmark : gap = 62 : 36 : 14), with one
deliberate change: the artboard's gap included the SVG's own internal padding,
which a cropped logo asset does not have, so the rendered gap is tightened from
165px to 90px at the master size. Optically that matches what the artboard
looked like.

Aspect ratio 5.564, so at the theme's `logo_height` of 36 it renders 200px wide.

## Monochrome on purpose

Brand red `#E3242B` is in the site palette but deliberately not in the mark. A
logo that needs two colours to carry its idea breaks on a label, an embroidery
file, or a 16px favicon. Red stays an accent for badges and UI.

## Live wiring

On theme `DRIPHOPE (cart-shipping-2026-10-02)` (id `154276560965`),
`config/settings_data.json`:

    "logo":    "shopify://shop_images/driphope_lockup_black.png"
    "favicon": "shopify://shop_images/driphope_icon_512.png"

`settings.logo` is a global theme setting, not a block setting — the
`_header-logo` block only carries `wordmark_text`, which is the text fallback
shown when no logo image is set. Setting `logo` replaces that text.

`logo_inverse` is left unset: it is only consulted when a transparent header is
enabled, and all three `enable_transparent_header_*` settings are false. If one
is ever turned on, point it at `driphope-lockup-white.png`.

## Superseded concepts

`driphope-01-drop-d-*`, `-02-dh-lock-*`, `-03-hard-drip-*`, `-04-cut-d-*` are an
earlier exploration, kept for reference. All four were two-tone by default, with
a red bar or red half carrying the idea; that is what made them read as unclean.
They are not in use.

Two other directions were drawn alongside the current mark and not chosen: a
bare teardrop (simplest, but reads as generic water rather than streetwear) and
a DH monogram (sober, least ownable).
