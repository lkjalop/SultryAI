import json
import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from sultrytai.api import app
from storage.sqlite_adapter import ensure_db, get_event, DB_PATH


client = TestClient(app)


def load_example():
    p = Path(__file__).resolve().parent.parent / "examples" / "example_event.json"
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def test_valid_event_is_accepted_and_persisted(tmp_path):
    # ensure fresh DB path in tmp to avoid clobbering developer DB
    # override module DB_PATH used by storage adapter
    DB_PATH = tmp_path / "sultry_test.db"
    # monkeypatch by assigning into the storage module
    import storage.sqlite_adapter as sdb

    sdb.DB_PATH = DB_PATH
    ensure_db()

    ev = load_example()
    headers = {"x-api-key": "demo-key-123"}
    r = client.post("/ingest/event", json=ev, headers=headers)
    assert r.status_code == 200 or r.status_code == 201 or r.status_code == 200
    body = r.json()
    assert body.get("status") == "accepted"
    event_id = body.get("event_id")
    assert event_id is not None

    stored = get_event(event_id)
    assert stored is not None


def test_invalid_event_is_rejected():
    # send an event missing required fields (remove event_id)
    ev = {"timestamp": "2025-01-01T00:00:00Z"}
    headers = {"x-api-key": "demo-key-123"}
    r = client.post("/ingest/event", json=ev, headers=headers)
    assert r.status_code == 400
    assert "schema" in r.json().get("detail", "").lower()
