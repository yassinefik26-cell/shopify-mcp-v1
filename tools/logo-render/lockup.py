#!/usr/bin/env python3
"""Render the DRIPHOPE horizontal lockup: Drop D mark + Archivo 800 wordmark.

Proportions are taken from the approved Lockup artboard, where the row is
icon box 62px / wordmark 36px / gap 14px, flex-centred. The wordmark is set
with -0.025em tracking, drawn glyph by glyph since PIL has no tracking control.
The mark's glyph is optically centred against the wordmark's cap height rather
than its em box, which is what the browser's all-caps centring looked like.
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import outer_poly, drop_poly, scale as _scale   # same geometry

FONT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Archivo-ExtraBold.ttf')
WORD = 'DRIPHOPE'
TRACK = -0.025          # em
BOX = 400               # the mark's 256-grid box, in px
FONT_PX = round(BOX * 36 / 62)
GAP = round(BOX * 14 / 62)
SS = 4                  # supersample


def mark_rgba(box, ink):
    """The Drop D at `box` px square, antialiased, in `ink`."""
    big = box * SS
    k = big / 256.0
    m = Image.new('L', (big, big), 0)
    d = ImageDraw.Draw(m)
    d.polygon(_scale(outer_poly(), k), fill=255)
    d.polygon(_scale(drop_poly(), k), fill=0)
    m = m.resize((box, box), Image.LANCZOS)
    img = Image.new('RGBA', (box, box), ink + (0,))
    img.putalpha(m)
    return img


def draw_word(size, ink):
    """DRIPHOPE with manual tracking; returns an RGBA image cropped to ink."""
    font = ImageFont.truetype(FONT, size * SS)
    track = TRACK * size * SS
    pad = size * SS
    canvas = Image.new('RGBA', (int(size * SS * len(WORD) * 1.2) + 2 * pad,
                                int(size * SS * 2)), ink + (0,))
    d = ImageDraw.Draw(canvas)
    x = float(pad)
    for ch in WORD:
        d.text((x, pad), ch, font=font, fill=ink + (255,))
        x += d.textlength(ch, font=font) + track
    return canvas.crop(canvas.getbbox()).resize(
        (max(1, (canvas.getbbox()[2] - canvas.getbbox()[0]) // SS),
         max(1, (canvas.getbbox()[3] - canvas.getbbox()[1]) // SS)),
        Image.LANCZOS)


def lockup(ink, out):
    mark = mark_rgba(BOX, ink)
    mark = mark.crop(mark.getbbox())            # tight to the glyph
    word = draw_word(FONT_PX, ink)

    h = max(mark.height, word.height)
    w = mark.width + GAP + word.width
    canvas = Image.new('RGBA', (w, h), ink + (0,))
    canvas.alpha_composite(mark, (0, (h - mark.height) // 2))
    canvas.alpha_composite(word, (mark.width + GAP, (h - word.height) // 2))
    canvas = canvas.crop(canvas.getbbox())
    canvas.save(out, optimize=True)
    print(f'  {os.path.basename(out):32s} {canvas.width}x{canvas.height}')


if __name__ == '__main__':
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    lockup((11, 11, 11), os.path.join(outdir, 'driphope-lockup-black.png'))
    lockup((255, 255, 255), os.path.join(outdir, 'driphope-lockup-white.png'))
