import random
from ..actions_base import Action, Contestant

class Attack(Action):
    def __init__(self, contestant: Contestant, opponent: Contestant):
        super().__init__(contestant)
        self.opponent = opponent
        self.duration = 2

    def resolve(self):
        self.opponent.take_damage(self.calculate_damage())

    def calculate_damage(self):
        base_dmg = self.contestant.stats.offensive_power * random.uniform(0.5, 5)
        base_dmg += random.uniform(0.5, 1.5) * self.contestant.weapon
        base_dmg -= random.uniform(0.5, 1.5) * self.opponent.armor

        return max(0, base_dmg)
