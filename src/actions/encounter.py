from copy import copy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.contestants.contestant import Contestant

class Encounter:
    """Maintain a persistent state of a fight encounter"""

    def __init__(self, contestants: list[Contestant]):
        """Initialise a combat encounter"""
        self.contestants = copy(contestants)
        self.active = True

    def contains(self, contestant: Contestant) -> bool:
        """Return whether a contestant is in current encounter"""
        return contestant in self.contestants

    def add_contestant(self, contestant: Contestant) -> None:
        """Add a contestant to current encounter"""
        if contestant not in self.contestants:
            self.contestants.append(contestant)
