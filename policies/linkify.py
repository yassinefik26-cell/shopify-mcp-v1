#!/usr/bin/env python3
"""Turn plain-text contact details in policy HTML into real links.

Visible text is never altered — only an <a> wrapper is added around it. That is
a hard rule: these are legal documents, so the words a customer reads must come
out byte-identical.

Addresses are matched as street + <br> + city/state/zip together so the whole
block becomes one link, the way a reader expects.
"""
import re

EMAIL_HREF = 'mailto:contact@driphope.com'
MAPS_HREF = ('https://www.google.com/maps/search/?api=1&amp;query='
             '301+East+E+Street%2C+Casper%2C+WY+82601%2C+United+States')

ADDRESS = re.compile(
    r'(301\s+EAST\s+E\s+STREET\s*<br\s*/?>\s*CASPER,\s*WY\s*\d{4,5}'
    r'(?:,\s*United\s+States)?)', re.I)
EMAIL = re.compile(r'([Cc]ontact@driphope\.com)')


def _protected(html):
    """Spans we must not touch: inside any tag, or already inside an <a>."""
    spans = [(m.start(), m.end()) for m in re.finditer(r'<[^>]*>', html)]
    spans += [(m.start(), m.end()) for m in re.finditer(r'<a\b[^>]*>.*?</a>', html, re.S | re.I)]
    return spans


def _sub_safe(html, pattern, wrap):
    """Apply `wrap` to matches that are neither inside a tag nor already linked."""
    prot = _protected(html)
    out, last, n = [], 0, 0
    for m in pattern.finditer(html):
        if any(a <= m.start() < b for a, b in prot):
            continue
        out.append(html[last:m.start()])
        out.append(wrap(m.group(1)))
        last = m.end()
        n += 1
    out.append(html[last:])
    return ''.join(out), n


def linkify(html):
    html, n_addr = _sub_safe(
        html, ADDRESS,
        lambda t: f'<a href="{MAPS_HREF}" target="_blank" rel="noopener">{t}</a>')
    html, n_mail = _sub_safe(
        html, EMAIL,
        lambda t: f'<a href="{EMAIL_HREF}">{t}</a>')
    return html, n_addr, n_mail


def visible_text(html):
    """Rendered text, for proving the reader-facing wording did not change."""
    t = re.sub(r'<br\s*/?>', '\n', html, flags=re.I)
    t = re.sub(r'<[^>]*>', '', t)
    t = t.replace('&nbsp;', ' ').replace('&amp;', '&')
    return re.sub(r'[ \t]+', ' ', t)
