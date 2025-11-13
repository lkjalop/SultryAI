from fastapi.testclient import TestClient
from sultrytai.api import app
from sensors import ConvoTrap, ScaleBait, PhishPuppet


def _assert_emit(sensor):
    client = TestClient(app)
    resp = sensor.emit_event(client)
    assert resp.status_code == 200
    data = resp.json()
    assert data.get('status') == 'accepted'
    event_id = data.get('event_id')
    assert event_id
    # fetch verdict (stored event)
    v = client.get(f"/verdict/{event_id}", headers={"x-api-key": "demo-key-123"})
    assert v.status_code == 200
    stored = v.json()
    assert stored.get('event_id') == event_id
    assert stored.get('event_type')


def test_convotrap_emit():
    _assert_emit(ConvoTrap())


def test_scalebait_emit():
    _assert_emit(ScaleBait())


def test_phishpuppet_emit():
    _assert_emit(PhishPuppet())
