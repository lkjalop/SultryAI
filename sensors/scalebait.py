import uuid
from datetime import datetime, timezone


class ScaleBait:
    """Minimal ScaleBait sensor stub.

    Simulates deployment of high-value bait (e.g., exposed APIs) to attract
    mass scanning and automated attacks. Provides a start/stop interface and
    simple emit_event for integration tests.
    """

    def __init__(self, name: str = "scalebait"):
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
            "sensor_type": "web",
            "event_type": "bait_hit",
            "meta": {"stub": True, "sensor": self.name},
        }
        resp = client.post("/ingest/event", json=payload, headers={"x-api-key": api_key})
        return resp
