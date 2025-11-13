import uuid
from datetime import datetime, timezone


class ConvoTrap:
    """Minimal ConvoTrap sensor stub.

    In production this would run an interactive chatbot-style trap and emit
    events to the SultryAI ingest API. This stub exposes a simple start/stop
    interface plus a basic emit_event for integration tests.
    """

    def __init__(self, name: str = "convotrap"):
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
        """Emit a minimal valid event payload via provided FastAPI TestClient.
        Expects ingest endpoint at /ingest/event.
        """
        payload = {
            "event_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "sensor_id": self.name + "-1",
            "sensor_type": "email",  # chatbot styled deception -> treat as email/other
            "event_type": "conversation_probe",
            "meta": {"stub": True, "sensor": self.name},
        }
        resp = client.post("/ingest/event", json=payload, headers={"x-api-key": api_key})
        return resp
