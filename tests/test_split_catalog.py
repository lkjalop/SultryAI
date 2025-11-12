from scripts.split_full_catalog import split_full
from pathlib import Path

def test_split_creates_index_and_files():
    idx = split_full()
    root = Path(__file__).parent.parent / 'factors_catalog'
    idx_path = root / 'index.json'
    assert idx_path.exists()
    assert isinstance(idx, dict)
    # Check files exist
    for dom, info in idx.items():
        f = root / info['file']
        assert f.exists()
        # basic sanity: array inside
        import json
        data = json.loads(f.read_text(encoding='utf-8'))
        assert isinstance(data, list)
        assert len(data) == info['count']
