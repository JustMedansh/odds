import random
from logger import Logger

class Event:
    def __init__(self, game):
         self.game = game
         self.logger: Logger = game.logger

    @staticmethod
    def get_power(tribute, weights):
        power = 0
        armor = tribute.armor
        weapon = tribute.weapon
        for stat, weight in weights.items():
            if stat == "random":
                continue

            if stat in tribute.skills:
                value = tribute.skills[stat]
            else:
                value = getattr(tribute, stat)

            power += value * weight 

        power += random.randint(-weights['random'], weights['random'])
        return power
