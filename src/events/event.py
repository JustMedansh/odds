from __future__ import annotations

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.contestants.contestant import Contestant
    from src.contestants.grouped_contestant import GroupedContestants
    from src.core.game import Game
    from src.logger import Logger

class Event:
    def __init__(self, gc: GroupedContestants, game: Game):
        self.gc = gc
        self.logger: Logger = game.logger
        self.game = game

    @staticmethod
    def get_power(contestant: Contestant, weights: dict[str, int]):
        """Calculate power with randomness and stats"""
        power = 0
        for stat, weight in weights.items():
            if stat == "random":
                continue

            if hasattr(contestant.personality, stat):
                value = getattr(contestant.personality, stat)
            else:
                value = getattr(contestant, stat)

            power += value * weight 

        power += random.randint(-weights['random'], weights['random'])
        return power
