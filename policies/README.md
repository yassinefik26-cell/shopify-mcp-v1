# Policy pages — contact details as real links

Ready-to-paste HTML for the five shop policies, with every plain-text contact
detail wrapped in a working link.

**These were NOT applied via the API.** `shopPolicyUpdate` is refused:

    Access denied for shopPolicyUpdate field.
    Required access: `write_legal_policies` access scope.

The connector does not hold that scope, so shop policies have to be pasted in
by hand. Theme files and navigation are writable; legal policies are not.

## How to paste

For each file: Shopify admin -> Settings -> Policies -> open the policy ->
click the `<>` (Show HTML) button in the editor toolbar -> select all ->
paste the file's contents -> Save.

The `<>` step matters. Pasting into the rich-text view would show the markup
as literal text instead of rendering it.

| file | policy | links added |
|---|---|---|
| `CONTACT_INFORMATION.html` | Contact information | 1 address |
| `LEGAL_NOTICE.html` | Legal notice | 1 address |
| `PRIVACY_POLICY.html` | Privacy policy | 3 address, 3 email |
| `REFUND_POLICY.html` | Refund policy | 2 address |
| `TERMS_OF_SERVICE.html` | Terms of service | 1 address, 1 email |

Shipping policy needed nothing — all six of its contact details were already
linked.

## What changed

12 links inserted: 8 Google Maps, 4 mailto. Phone numbers were already `tel:`
links everywhere, so none were touched.

Street and city/state are wrapped as ONE anchor spanning the `<br>` between
them, so the address reads and behaves as a single link.

All eight address links point at the same canonical query:

    https://www.google.com/maps/search/?api=1&query=301+East+E+Street%2C+Casper%2C+WY+82601%2C+United+States

Four deliberate wording corrections, approved separately:

| where | before | after |
|---|---|---|
| Privacy §1 | `CASPER, WY 8260` | `CASPER, WY 82601` |
| Refund §2 | `CASPER, WY 8260` | `CASPER, WY 82601` |
| Privacy §10 | `Contact@driphope.com` | `contact@driphope.com` |
| Terms §20 | `Contact@driphope.com` | `contact@driphope.com` |

The ZIP was a four-digit truncation, and the Refund one sits in a return
address, so it risked misrouted mail. The capitalised local-part was
inconsistent with the other nineteen occurrences across the store.

## How it was generated

`linkify.py`. It refuses to write a file unless the rendered text — tags
stripped — is byte-identical to the input apart from those four approved
corrections. These are legal documents; the words a customer reads must not
drift because of a markup change.

It also skips any match that sits inside a tag or inside an existing `<a>`,
so re-running it is idempotent and it never double-wraps an already-linked
detail or mangles an `href="mailto:…"` attribute.

## Still open

`/pages/payment-policy` is linked from the footer and is **completely empty**.
Customers clicking "Payment Policy" land on a blank page. Unlike the policies
above, ordinary pages are writable through the API, so that one can be filled
from here once there is content for it.
