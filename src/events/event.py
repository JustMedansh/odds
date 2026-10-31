import random
from src.contestants.contestant import Contestant
from src.logger import Logger
from src.contestants.grouped_contestant import GroupedContestants

class Event:
    def __init__(self, game: GroupedContestants):
        self.game = game
        self.logger: Logger = game.logger

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
