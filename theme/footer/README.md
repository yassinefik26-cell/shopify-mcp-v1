# Footer rebuild — three columns

Rebuilt to the merchant's reference layout: policies links | business contact |
newsletter.

Deployed to `DRIPHOPE (phone-2026-10-10)`, theme id `154638188613`, UNPUBLISHED.
Live theme writes are blocked by the connector, so every change lands on a
duplicate the merchant publishes themselves.

| file | bytes | md5 |
|---|---|---|
| `blocks/footer-contact.liquid` | 4874 | `02d936022003441a77389c15fdac7a18` |
| `sections/footer-group.json` | 13555 | `efc9d2094299076fb78603fa4cbe6f80` |

## Column 1 — "Our policies"

A `menu` block bound to a NEW navigation menu, handle `footer-policies`
(`gid://shopify/Menu/250096123973`), so the links are editable in
Admin → Navigation without touching code.

A new menu was created rather than editing the existing `footer` menu on
purpose: navigation is store-level, not theme-level, so editing `footer` would
have changed the live storefront immediately — before the merchant had seen
anything.

| label | target | resolved |
|---|---|---|
| Search | SEARCH | `/search` |
| Privacy Policy | SHOP_POLICY `44794642501` | `/policies/privacy-policy` |
| Refund Policy | SHOP_POLICY `44894650437` | `/policies/refund-policy` |
| Shipping Policy | SHOP_POLICY `45092405317` | `/policies/shipping-policy` |
| Terms of Service | SHOP_POLICY `45059801157` | `/policies/terms-of-service` |
| Payment Policy | PAGE `123165507653` | `/pages/payment-policy` |
| Track your order | HTTP | `/apps/track123` — **unverified** |

"Payment Policy" is not a Shopify policy type; it already existed as an ordinary
page, so the item points there.

"Track your order" had no existing page or policy. Track123 is installed, so the
item points at that app's conventional proxy path. **This path is a guess** —
confirm it in the Track123 app and correct it in Navigation if wrong. No code
change needed.

## Column 2 — "About Us"

`blocks/footer-contact.liquid`, a block written for this, with one editable
field per value. The merchant never edits code to change a number:

| setting | default |
|---|---|
| `company_name` | DRIPHOPE LLC |
| `address` | 301 East E Street, Casper, WY 82601 |
| `email` | contact@driphope.com |
| `phone` | +1 (914) 436-2237 |
| `support_days` | Monday – Friday |
| `timezone` | MT |
| `response_time` | 24–48 business hours |

`timezone` renders in brackets after the support days and is skipped when
blank. It was briefly ET, reasoning from the 914 area code, then set to MT to
follow the registered address in Casper, WY.

Note this does NOT follow the store's own timezone setting, which is
`Africa/Casablanca` (where the merchant operates). The Admin API exposes no
mutation to change that — all 454 mutations were enumerated and the only
shop-level ones are `shopLocaleUpdate`, `shopPolicyUpdate`,
`shopResourceFeedbackCreate` and payments. Settings > General is admin-UI only.

There is deliberately no WhatsApp row: the merchant removed it.

The `tel:` href is DERIVED from what is typed, so the number lives in exactly
one field. Liquid has no regex replace, so separators are stripped one filter
at a time.

The address default is a single line because a schema default cannot safely
carry a `\n` (see below). The field is a textarea, so pressing Enter in the
theme editor splits it across rows.

Every row is wrapped in `{% if ... != blank %}`, so an empty field drops its
row rather than leaving a dangling label.

The block is listed in `footer-group.json` with `"settings": {}`, which makes it
fall back to the schema defaults above — the same pattern used by the
product-info block.

### Do not reintroduce a `\n` in the schema

The `address` default originally carried a literal `\n`. Escaping a backslash
through this connector's GraphQL transport is unreliable: an earlier upload in
this project wrote `\\u00a0` and the stored file came back with a real U+00A0,
meaning the escape was processed somewhere in transit. A real newline inside the
schema's JSON string is invalid JSON and would break the block silently. The
file now contains zero backslashes; keep it that way.

## Column 3 — "Join Our Journey"

Heading, a blurb, the theme's native `email-signup` block carried over with its
existing settings (red `#e3242b` button, pill radius), and the social links
block beneath it.

The store has **no Klaviyo**. Installed apps are Messaging, POKY, Track123,
Simprosys Google Shopping Feed and the Claude connectors. The signup is
Shopify's built-in customer email capture, which is what the previous footer
used too.

The blurb is original copy, not the reference image's wording — that text
belongs to another store.

## Social links

`social_links_driphope` sits last in column 3, which is where it lived in the
previous footer (inside the newsletter group). Its settings were copied from the
live theme verbatim, so the four live URLs are unchanged:

    instagram  https://www.instagram.com/driphope2320/
    youtube    https://www.youtube.com/channel/UCHLncrEJyQUNOcEGsOI18nA
    tiktok     https://www.tiktok.com/@driphope0
    pinterest  https://www.pinterest.com/Driphope13/_profile/

## What the rebuild dropped

The standalone `text_phone_driphope` block from the previous change is gone; the
phone now lives in the contact block's Phone row instead.

## Styling notes

The requested palette was "black/cream/camel/bordeaux". The store's actual
palette is black/white/grey with a red accent:

    background #ffffff   foreground #111111
    color1 #141414       color2 #F2F1EF       color3 #E2E2E2
    accent #E3242B

The footer already sits on `color1` (#141414), so the dark ground matches. No
cream, camel or bordeaux exists in the theme — introducing them means editing
the palette in Theme settings, which would affect the whole store, not just the
footer. Left alone deliberately.

Typography likewise: the reference's headings are a serif, the theme's heading
font is Inter (`inter_n7`). The footer headings render in Inter. Matching the
reference would mean changing the theme's heading font globally.
