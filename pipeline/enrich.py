from typing import Dict, Any

def enrich_event(event: Dict[str, Any]) -> Dict[str, Any]:
    ev = dict(event)
    # basic enrichment: mark honeypot if sensor_id contains 'honeypot' or 'convotrap'
    sensor = ev.get('sensor_id','') or ''
    ev['meta'] = ev.get('meta',{})
    if 'honeypot' in sensor or 'convotrap' in sensor or 'phishpuppet' in sensor:
        ev['meta']['honeypot'] = True
    return ev
