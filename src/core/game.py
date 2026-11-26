class Game:
    """Orchestrates an ODDS simulation."""

    def __init__(self, contestants, world_map):
        self.contestants = contestants
        self.world_map = world_map

        self.running = False
        self.tick_count = 0

    def start(self):
        """Start the simulation."""
        self.running = True
        return self.run()

    def run(self):
        """Keep the simulation running on a tick-by-tick basis"""
        while self.running:
            self.tick()
        self.end()

    def tick(self):
        """Advance the simulation by one tick."""
        if not self.running:
            return False

        self.tick_count += 1

        if not True: # TERMINATION CONDITION
            return True
        return False

    def end(self):
        """End the simulation."""
        self.running = False
