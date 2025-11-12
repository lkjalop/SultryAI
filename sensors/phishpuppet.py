class PhishPuppet:
    """Minimal PhishPuppet sensor stub.

    Represents email/phishing-style deception sensors that record interactions.
    Provides a tiny interface suitable for unit tests and local runs.
    """

    def __init__(self, name: str = "phishpuppet"):
        self.name = name
        self.running = False

    def start(self):
        self.running = True
        return f"{self.name} started"

    def stop(self):
        self.running = False
        return f"{self.name} stopped"
