import json, sys
sys.path.insert(0, '.')
from care import CARE

def bullets(text):
    """Split ARNE's run-on sentences into one bullet per sentence, verbatim."""
    parts = [p.strip() for p in text.split('. ')]
    out = []
    for p in parts:
        p = p.rstrip('.').strip()
        if p:
            out.append(p)
    return '\n'.join(out)

rows = [l.rstrip('\n').split('\t') for l in open('all.tsv') if l.strip()]
recs = []
for pid, fabric, ckey in rows:
    recs.append({
        'id': f'gid://shopify/Product/{pid}',
        'metafields': [
            {'namespace': 'custom', 'key': 'composition',
             'type': 'multi_line_text_field', 'value': bullets(fabric)},
            {'namespace': 'custom', 'key': 'care_instructions',
             'type': 'multi_line_text_field', 'value': bullets(CARE[ckey])},
        ],
    })

json.dump(recs, open('recs.json', 'w'), ensure_ascii=False)

if len(sys.argv) > 1:
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    sel = recs[lo:hi]
    n = len(sel)
    decl = ', '.join(f'$p{i}: ProductUpdateInput!' for i in range(n))
    body = '\n'.join(f'  u{i}: productUpdate(product: $p{i}) {{ userErrors {{ field message }} }}' for i in range(n))
    print('=== QUERY ===')
    print(f'mutation mf({decl}) {{\n{body}\n}}')
    print('=== VARIABLES ===')
    print(json.dumps({f'p{i}': r for i, r in enumerate(sel)}, separators=(',', ':'), ensure_ascii=False))
    print(f'=== {n} products, {n*2} metafields ===')
else:
    print(f'records: {len(recs)}  metafields: {len(recs)*2}')
    print('\n--- sample: hoodie ---')
    s = next(r for r in recs if r['id'].endswith('8296417689669'))
    print('composition:', repr(s['metafields'][0]['value']))
    print('care       :', repr(s['metafields'][1]['value']))
    print('\n--- sample: backpack (multi-part fabric) ---')
    s = next(r for r in recs if r['id'].endswith('8297018392645'))
    print('composition:', repr(s['metafields'][0]['value']))
    print('care       :', repr(s['metafields'][1]['value']))
