import json
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
FULL = ROOT / 'factors_catalog' / 'full' / 'factors_catalog_full.json'
OUT_DIR = ROOT / 'factors_catalog'

def split_full():
    if not FULL.exists():
        raise FileNotFoundError(str(FULL))
    with FULL.open('r', encoding='utf-8') as f:
        items = json.load(f)
    groups = defaultdict(list)
    for it in items:
        dom = it.get('domain','other')
        groups[dom].append(it)
    index = {}
    for dom, entries in groups.items():
        path = OUT_DIR / f'factors_{dom}.json'
        with path.open('w', encoding='utf-8') as f:
            json.dump(entries, f, indent=2)
        index[dom] = {'file': path.name, 'count': len(entries)}
    # write index.json
    idx_path = OUT_DIR / 'index.json'
    with idx_path.open('w', encoding='utf-8') as f:
        json.dump(index, f, indent=2)
    return index

if __name__ == '__main__':
    idx = split_full()
    print('Wrote index:', idx)
