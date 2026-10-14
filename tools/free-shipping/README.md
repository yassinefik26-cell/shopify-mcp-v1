# Free shipping — delivery rates zeroed

The cart now states "Free shipping on all orders." The rates were
set to zero so that statement is true.

## Before

Shop currency: MAD. One delivery profile, `General profile` (default), id
`103003881541`, one location group `104408907845` (location `wanda`).

| zone | countries | method | rate before | rate after |
|---|---|---|---|---|
| Domestic | Morocco | Standard | **34.00 MAD** | 0.00 MAD |
| International | 28 countries | International | **180.00 MAD** | 0.00 MAD |

International zone: AE AT AU BE CA CH CZ DE DK ES FI FR GB HK IE IL IT JP KR MY
NL NO NZ PL PT SE SG US.

Both methods are `DeliveryRateDefinition` (flat rates). There are no carrier
services / `DeliveryParticipant` rates and no second delivery profile, so these
two rates covered every order the store can accept.

## Scope of the claim

"All orders" means all orders the store can accept. Countries outside the two
zones have no rate at all and cannot check out — that was already true before
this change and is unaffected by it.

## Revert

    mutation freeShipping($id: ID!, $profile: DeliveryProfileInput!) {
      deliveryProfileUpdate(id: $id, profile: $profile) {
        userErrors { field message }
      }
    }

    {
      "id": "gid://shopify/DeliveryProfile/103003881541",
      "profile": { "locationGroupsToUpdate": [{
        "id": "gid://shopify/DeliveryLocationGroup/104408907845",
        "zonesToUpdate": [
          { "id": "gid://shopify/DeliveryZone/380920168517",
            "methodDefinitionsToUpdate": [{
              "id": "gid://shopify/DeliveryMethodDefinition/825792888901",
              "rateDefinition": {
                "id": "gid://shopify/DeliveryRateDefinition/760038457413",
                "price": { "amount": "34.0", "currencyCode": "MAD" } } }] },
          { "id": "gid://shopify/DeliveryZone/380920201285",
            "methodDefinitionsToUpdate": [{
              "id": "gid://shopify/DeliveryMethodDefinition/825792921669",
              "rateDefinition": {
                "id": "gid://shopify/DeliveryRateDefinition/760038490181",
                "price": { "amount": "180.0", "currencyCode": "MAD" } } }] }
        ] }] }
    }

Or in admin: Settings -> Shipping and delivery -> General profile -> each zone ->
edit the rate.

Note that zeroing a rate and deleting it are different: a zero rate still gives
the customer a selectable "Standard" / "International" option at checkout, which
is what makes free shipping appear. Deleting the rate would block checkout.
