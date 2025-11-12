import re
from pathlib import Path

FULL = Path(__file__).parent.parent / 'factors_catalog' / 'full' / 'factors_catalog_full.json'

def clean():
    text = FULL.read_text(encoding='utf-8')
    # Replace any pattern of ']' whitespace '[' with ',' to merge arrays
    new = re.sub(r"\]\s*\[", ",", text)
    # Ensure the result is a single JSON array: if multiple leading/trailing brackets exist, normalize
    # Collapse beginning like '[[' -> '[' and ']]' -> ']'
    new = re.sub(r"\[\s*\[", "[", new)
    new = re.sub(r"\]\s*\]", "]", new)
    FULL.write_text(new, encoding='utf-8')
    print('Cleaned', FULL)

if __name__ == '__main__':
    clean()
