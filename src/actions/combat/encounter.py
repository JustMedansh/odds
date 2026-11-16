from copy import copy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.contestants.contestant import Contestant

class Encounter:
    """Maintain a persistent state of a combat encounter"""

    def __init__(self, contestants: list[Contestant]):
        """Initialise a combat encounter"""
        self.contestants = copy(contestants)
        self.active = True

        self.contestants_status = {c: True for c in self.contestants}

    def contains(self, contestant: Contestant) -> bool:
        """Return whether a contestant is in current encounter"""
        return contestant in self.contestants

    def add_contestant(self, contestant: Contestant) -> None:
        """Add a contestant to current encounter"""
        if self.active and contestant not in self.contestants:
            self.contestants.append(contestant)
            self.contestants_status[contestant] = True

    def remove_contestant(self, contestant: Contestant) -> None:
        """Remove contestant from encounter. Raises ValueError if contestant doesn't exist."""
        self.contestants.remove(contestant)
        self.contestants_status[contestant] = False

    def get_all_contestants(self) -> list[Contestant]:
        """Get a list of all active contestants in encounter"""
        return [c for c in self.contestants if self.contestants_status[c]]

    @property
    def size(self) -> int:
        """Get number of contestants in encounter"""
        return len(self.contestants)

    def end(self) -> None:
        """End the encounter"""
        self.active = False
