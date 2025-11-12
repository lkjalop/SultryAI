import os
import tempfile
import json
from sultrytai import api as api_mod
from storage.sqlite_adapter import insert_event, get_event, DB_PATH

def test_pipeline_score_and_persist(tmp_path, monkeypatch):
    # create a temporary DB path
    monkeypatch.setattr(api_mod, 'catalog', api_mod.catalog)
    # build event
    ev = {
        "event_id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
        "timestamp": "2025-11-13T12:00:00Z",
        "sensor_id": "convotrap-01",
        "sensor_type": "ssh",
        "event_type": "cmd_exec",
        "command": "whoami"
    }
    # call pipeline functions directly
    from pipeline.normalize import normalize_event
    from pipeline.enrich import enrich_event
    from pipeline.score import score_event

    n = normalize_event(ev)
    e = enrich_event(n)
    s = score_event(e)

    # persist
    insert_event(s)
    got = get_event(s['event_id'])
    assert got is not None
    assert got['event_id'] == s['event_id']
    assert got.get('score') is not None
