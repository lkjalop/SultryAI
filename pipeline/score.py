from typing import Dict, Any

def score_event(event: Dict[str, Any]) -> Dict[str, Any]:
    ev = dict(event)
    # simple scoring: base score for honeypot interaction
    ev['score'] = {
        'base': 0.0,
        'factors': []
    }
    if ev.get('meta',{}).get('honeypot'):
        ev['score']['base'] = 0.9
        ev['score']['factors'].append({'name':'honeypot_interaction','severity':0.9})
    return ev
