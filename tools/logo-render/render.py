#!/usr/bin/env python3
"""Rasterise the DRIPHOPE Drop D mark from its exact SVG geometry.

No SVG rasteriser is installed, so the two paths are flattened here by hand and
drawn into a high-resolution coverage mask, then downsampled with LANCZOS for
antialiasing. The numbers mirror brand/logo/driphope-mark-black.svg exactly:

  outer  M48 40 H120 A88 88 0 0 1 120 216 H48 Z
  drop   M126 71 C108 104 82 124 82 146 A44 44 0 1 0 170 146 C170 124 144 104 126 71 Z
"""
import math, os, sys
from PIL import Image, ImageDraw

BASE = 2048          # mask resolution; 8x the 256 design grid
S = BASE / 256.0
STEPS = 512          # flattening resolution per curve


def bezier(p0, p1, p2, p3, steps=STEPS):
    out = []
    for i in range(steps + 1):
        t = i / steps
        u = 1 - t
        x = u*u*u*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t*t*t*p3[0]
        y = u*u*u*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t*t*t*p3[1]
        out.append((x, y))
    return out


def semicircle(cx, cy, r, kind, steps=STEPS):
    """kind 'right': top->right->bottom.  kind 'down': left->bottom->right."""
    out = []
    for i in range(steps + 1):
        t = i / steps
        a = math.pi * t
        if kind == 'right':
            out.append((cx + r*math.sin(a), cy - r*math.cos(a)))
        else:
            out.append((cx - r*math.cos(a), cy + r*math.sin(a)))
    return out


def outer_poly():
    pts = [(48, 40), (120, 40)]
    pts += semicircle(120, 128, 88, 'right')
    pts += [(48, 216)]
    return pts


def drop_poly():
    pts = [(126, 71)]
    pts += bezier((126, 71), (108, 104), (82, 124), (82, 146))
    pts += semicircle(126, 146, 44, 'down')
    pts += bezier((170, 146), (170, 124), (144, 104), (126, 71))
    return pts


def scale(pts, k=S, dx=0.0, dy=0.0):
    return [((x * k) + dx, (y * k) + dy) for x, y in pts]


def mark_mask(inner_scale=1.0):
    """Coverage mask of the mark on a BASE x BASE field, optionally inset."""
    m = Image.new('L', (BASE, BASE), 0)
    d = ImageDraw.Draw(m)
    k = S * inner_scale
    off = (BASE - 256 * k) / 2.0
    d.polygon(scale(outer_poly(), k, off, off), fill=255)
    d.polygon(scale(drop_poly(), k, off, off), fill=0)
    return m


def save(img, path, size):
    img.resize((size, size), Image.LANCZOS).save(path, optimize=True)
    print(f'  {os.path.basename(path):34s} {size}x{size}')


def main(outdir):
    os.makedirs(outdir, exist_ok=True)

    mask = mark_mask()

    # transparent-background mark, in each ink
    for name, ink in (('black', (11, 11, 11)), ('white', (255, 255, 255))):
        img = Image.new('RGBA', (BASE, BASE), ink + (0,))
        img.putalpha(mask)
        save(img, os.path.join(outdir, f'driphope-mark-{name}-512.png'), 512)

    # app icon: black squircle, white mark at 72%
    sq = Image.new('L', (BASE, BASE), 0)
    ImageDraw.Draw(sq).rounded_rectangle([0, 0, BASE - 1, BASE - 1],
                                         radius=60 * S, fill=255)
    white = Image.new('RGBA', (BASE, BASE), (255, 255, 255, 255))

    # Optical sizing: the glyph is inset 28% on a large app icon, but at favicon
    # sizes that padding eats the mark and the drop counter closes up, so the
    # small cuts carry a bigger glyph. Standard favicon practice, and the reason
    # these are separate files rather than one image scaled down.
    for size, inset in ((512, 0.72), (192, 0.72), (180, 0.72),
                        (32, 0.88), (16, 0.94)):
        icon = Image.new('RGBA', (BASE, BASE), (11, 11, 11, 0))
        icon.putalpha(sq)
        icon = Image.composite(white, icon, mark_mask(inset))
        icon.putalpha(sq)                  # re-apply the squircle edge
        save(icon, os.path.join(outdir, f'driphope-appicon-{size}.png'), size)


if __name__ == '__main__':
    main(sys.argv[1])
