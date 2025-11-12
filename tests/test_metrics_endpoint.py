from fastapi.testclient import TestClient
from sultrytai.api import app


def test_metrics_endpoint():
    client = TestClient(app)
    resp = client.get('/metrics')
    assert resp.status_code == 200
    ct = resp.headers.get('content-type','')
    assert 'text/plain' in ct or 'application/openmetrics-text' in ct
