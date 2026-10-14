#!/usr/bin/env python3
"""Replace every tax/duties/shipping-at-checkout locale value with a flat message.

Operates line-wise on the exact original bytes so that invisible characters
(U+00A0), `//` comments and line endings survive untouched. Refuses to write
unless the source checksum matches and ONLY the intended lines changed.

  python3 patch-locales.py fr.json  out.json "Livraison gratuite sur toutes les commandes." <md5>
"""
import hashlib, json, re, sys

KEYS = [
    "duties_and_taxes_included",
    "duties_and_taxes_included_shipping_at_checkout_with_policy_html",
    "duties_and_taxes_included_shipping_at_checkout_with_policy_without_discounts_html",
    "duties_and_taxes_included_shipping_at_checkout_without_policy",
    "duties_and_taxes_included_shipping_at_checkout_without_policy_without_discounts",
    "duties_included",
    "duties_included_taxes_at_checkout_shipping_at_checkout_with_policy_html",
    "duties_included_taxes_at_checkout_shipping_at_checkout_with_policy_without_discounts_html",
    "duties_included_taxes_at_checkout_shipping_at_checkout_without_policy",
    "duties_included_taxes_at_checkout_shipping_at_checkout_without_policy_without_discounts",
    "shipping_policy",
    "shipping_policy_html",
    "taxes_at_checkout_shipping_at_checkout_with_policy_html",
    "taxes_at_checkout_shipping_at_checkout_with_policy_without_discounts_html",
    "taxes_at_checkout_shipping_at_checkout_without_policy",
    "taxes_at_checkout_shipping_at_checkout_without_policy_without_discounts",
    "taxes_included",
    "taxes_included_shipping_at_checkout_with_policy_html",
    "taxes_included_shipping_at_checkout_with_policy_without_discounts_html",
    "taxes_included_shipping_at_checkout_without_policy",
    "taxes_included_shipping_at_checkout_without_policy_without_discounts",
]


def main(src, dst, newval, expect_md5):
    raw = open(src, "rb").read()
    got = hashlib.md5(raw).hexdigest()
    if got != expect_md5:
        sys.exit(f"source checksum drift: {got} != {expect_md5}")

    lines = raw.split(b"\n")
    changed = {}
    for key in KEYS:
        pat = re.compile(rb'^(    "' + re.escape(key.encode()) + rb'": )(".*")(,?)(\r?)$')
        hits = [i for i, l in enumerate(lines) if pat.match(l)]
        if len(hits) != 1:
            sys.exit(f"{key}: expected exactly 1 matching line, found {len(hits)}")
        m = pat.match(lines[hits[0]])
        lines[hits[0]] = (m.group(1)
                          + json.dumps(newval, ensure_ascii=False).encode()
                          + m.group(3) + m.group(4))
        changed[key] = hits[0]

    old = raw.split(b"\n")
    diff = {i for i in range(len(old)) if old[i] != lines[i]}
    if diff != set(changed.values()):
        sys.exit(f"unintended lines changed: {sorted(diff - set(changed.values()))}")

    out = b"\n".join(lines)
    txt = out.decode("utf-8")
    body = re.sub(r"^\s*//.*$", "", txt[txt.index("*/") + 2:], flags=re.M)
    obj = json.loads(body)                       # must still parse
    for k in KEYS:
        assert obj["content"][k] == newval, k

    open(dst, "wb").write(out)
    print(f"{dst}: {len(out)} bytes  md5={hashlib.md5(out).hexdigest()}  "
          f"({len(diff)} lines changed)")


if __name__ == "__main__":
    main(*sys.argv[1:5])
