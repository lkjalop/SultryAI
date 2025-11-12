class ConvoTrap:
    """Minimal ConvoTrap sensor stub.

    In production this would run an interactive chatbot-style trap and emit
    events to the SultryAI ingest API. This stub exposes a simple start/stop
    interface for tests and integration.
    """

    def __init__(self, name: str = "convotrap"):
        self.name = name
        self.running = False

    def start(self):
        self.running = True
        return f"{self.name} started"

    def stop(self):
        self.running = False
        return f"{self.name} stopped"
