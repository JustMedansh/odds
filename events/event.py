import random
from src.contestant import Contestant
from src.logger import Logger
from src.game import Game

class Event:
    def __init__(self, game: Game):
        self.game = game
        self.logger: Logger = game.logger

    @staticmethod
    def get_power(contestant: Contestant, weights: dict[str, int]):
        """Calculate power with randomness and stats"""
        power = 0
        for stat, weight in weights.items():
            if stat == "random":
                continue

            if stat in contestant.skills:
                value = contestant.skills[stat]
            else:
                value = getattr(contestant, stat)

            power += value * weight 

        power += random.randint(-weights['random'], weights['random'])
        return power
