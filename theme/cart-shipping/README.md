# Cart shipping message — "Livraison gratuite sur toutes les commandes."

Replaces the stock Horizon tax/duties/shipping note under the cart total with a
flat free-shipping statement, in French and English.

## What the cart used to say

    Droits de douane et taxes inclus. L'expédition est calculée lors du paiement.

## Where that text comes from

`snippets/cart-summary.liquid` delegates the note to `snippets/tax-info.liquid`,
which picks one of 16 branches:

    cart.duties_included  x  cart.taxes_included        (4 combinations)
      x  shop.shipping_policy.body == blank             (policy link / no link)
      x  has_discounts_enabled                          (settings.show_add_discount_code)

Each branch resolves a different `content.*` key, so changing only the string the
cart happens to render today would leave the old wording reachable as soon as the
store's tax settings, shipping policy or discount setting changed. All variants
are therefore replaced.

`tax-info.liquid` itself is NOT modified — only the locale values it resolves.

## Keys replaced (21, all under `content`)

The 14 keys `tax-info.liquid` can actually resolve:

    duties_and_taxes_included_shipping_at_checkout_with_policy_html
    duties_and_taxes_included_shipping_at_checkout_with_policy_without_discounts_html
    duties_and_taxes_included_shipping_at_checkout_without_policy
    duties_and_taxes_included_shipping_at_checkout_without_policy_without_discounts
    duties_included_taxes_at_checkout_shipping_at_checkout_with_policy_html
    duties_included_taxes_at_checkout_shipping_at_checkout_with_policy_without_discounts_html
    duties_included_taxes_at_checkout_shipping_at_checkout_without_policy
    duties_included_taxes_at_checkout_shipping_at_checkout_without_policy_without_discounts
    taxes_at_checkout_shipping_at_checkout_with_policy_html
    taxes_at_checkout_shipping_at_checkout_with_policy_without_discounts_html
    taxes_at_checkout_shipping_at_checkout_without_policy
    taxes_at_checkout_shipping_at_checkout_without_policy_without_discounts
    taxes_included_shipping_at_checkout_with_policy_html
    taxes_included_shipping_at_checkout_without_policy

Plus 7 more siblings that carry the same wording elsewhere (product page, or
currently unreferenced), so the phrasing cannot resurface:

    duties_and_taxes_included
    duties_included
    shipping_policy
    shipping_policy_html
    taxes_included
    taxes_included_shipping_at_checkout_with_policy_without_discounts_html
    taxes_included_shipping_at_checkout_without_policy_without_discounts

New values:

    locales/fr.json          Livraison gratuite sur toutes les commandes.
    locales/en.default.json  Free shipping on all orders.

The `_html` keys previously interpolated `{{ link }}` (the shipping-policy URL).
The new value takes no argument; the now-unused `t: link:` argument in
`tax-info.liquid` is harmless.

## Caveat: tax disclosure

Four of the replaced keys were the store's only tax-inclusive price disclosure
("Taxes incluses." / "Frais de douane et taxes inclus."). The store ships to 28
countries including the EU, where indicating whether tax is included in the
displayed price is a legal requirement. If that disclosure needs to come back,
use a combined value rather than restoring the old string, e.g.

    Taxes incluses. Livraison gratuite sur toutes les commandes.

## Shipping rates

The message is only truthful because the rates were zeroed at the same time —
see `tools/free-shipping/README.md`.

## Line endings and invisible characters

`locales/fr.json` contains 49 U+00A0 NO-BREAK SPACE characters (French
typography: before `!` `?` `:`, inside `« »`, and between `{{ count }}` and the
noun it quantifies). They are invisible in most renderings and are easy to
destroy when a locale file is retyped by hand — doing so silently changes the
typography of ~40 unrelated strings.

The files here are byte-exact. Both were produced by patching the exact original
bytes, never by retyping:

| file | bytes | md5 |
|---|---|---|
| `locales/fr.json` | 17811 | `77ffbe12b367e1f3a260ccc9add5381f` |
| `locales/en.default.json` | 16752 | `7a2158e9a4a7c3a3957f0831990ad015` |

Originals, for reference:

| file | bytes | md5 |
|---|---|---|
| `locales/fr.json` | 18474 | `c34ab851193e6f5d25e62d79e4a49aa8` |
| `locales/en.default.json` | 17377 | `a76f218891f1c738a81e6082fe95dbf4` |

`fr.json` is stored with all-CRLF endings. The original mixed LF (the
auto-generated comment header) with CRLF (the JSON body); normalising is
cosmetic and does not affect parsing.

`en.default.json` keeps its `//` line comments, so it is not valid strict JSON —
patch it line-wise, never by parse-and-re-emit.

## Deployed to

`DRIPHOPE (cart-shipping-2026-10-02)` — theme id `154276560965`, a duplicate of
the then-live `DRIPHOPE (size-guide-2026-10-02)` (`154274562117`). Writes to the
live theme are blocked by the connector's safety policy, so each change goes to a
fresh duplicate which the merchant then publishes.
