import uuid
from datetime import datetime, timezone


class PhishPuppet:
    """Minimal PhishPuppet sensor stub.

    Represents email/phishing-style deception sensors that record interactions.
    Provides a tiny interface suitable for unit tests and local runs plus
    emit_event for integration testing.
    """

    def __init__(self, name: str = "phishpuppet"):
        self.name = name
        self.running = False

    def start(self, auto_emit: bool = False, client=None):
        self.running = True
        if auto_emit and client is not None:
            self.emit_event(client)
        return f"{self.name} started"

    def stop(self):
        self.running = False
        return f"{self.name} stopped"

    def emit_event(self, client, api_key: str = "demo-key-123"):
        payload = {
            "event_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "sensor_id": self.name + "-1",
            "sensor_type": "email",
            "event_type": "phish_lure_opened",
            "meta": {"stub": True, "sensor": self.name},
        }
        resp = client.post("/ingest/event", json=payload, headers={"x-api-key": api_key})
        return resp
