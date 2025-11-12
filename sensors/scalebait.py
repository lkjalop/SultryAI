class ScaleBait:
    """Minimal ScaleBait sensor stub.

    Simulates deployment of high-value bait (e.g., exposed APIs) to attract
    mass scanning and automated attacks. Provides a start/stop interface.
    """

    def __init__(self, name: str = "scalebait"):
        self.name = name
        self.running = False

    def start(self):
        self.running = True
        return f"{self.name} started"

    def stop(self):
        self.running = False
        return f"{self.name} stopped"
