# Logo rasteriser

No SVG rasteriser is installed in this environment (no rsvg-convert, inkscape,
cairosvg or headless Chromium), so these two scripts flatten the mark's path
geometry by hand and draw it with Pillow.

    python3 -I render.py ../../brand/logo/png      # mark + app icon PNGs
    python3 -I lockup.py ../../brand/logo/png      # horizontal lockup PNGs

`render.py` holds the geometry and is imported by `lockup.py`; the numbers
mirror `brand/logo/driphope-mark-black.svg` exactly. Curves are flattened at 512
segments and drawn into a 2048px coverage mask, then downsampled with LANCZOS.

`Archivo-ExtraBold.ttf` is the Google Fonts Archivo 800 latin subset, converted
from woff2 with fontTools so Pillow can read it. SIL Open Font License.

## Optical sizing

The app icon insets the glyph by 28% at 512/192/180px. At 32 and 16px that
padding eats the mark and the drop counter closes up, so those cuts carry a
bigger glyph (12% and 6% inset). That is why they are separate files rather than
one image scaled down.

16px is soft no matter what — the stem and bowl blur together at that size. It
is legible but not crisp, which is inherent to a D with a counter. Shopify
generates its own sizes from the single uploaded 512px file, so the small cuts
here are reference only.
