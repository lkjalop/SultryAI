from typing import Dict, Any

def normalize_event(event: Dict[str, Any]) -> Dict[str, Any]:
    # minimal normalization: ensure timestamp and schema_version
    ev = dict(event)
    ev.setdefault('schema_version', '1.0')
    # TODO: expand normalization rules (ip canonicalization, timestamp parsing)
    return ev
