from __future__ import annotations

from typing import TYPE_CHECKING

import random
from ..actions_base import Action

if TYPE_CHECKING:
    from src.contestants import Contestant

class Attack(Action):
    def __init__(self, contestant: Contestant, opponent: Contestant):
        super().__init__(contestant)
        self.opponent = opponent
        self.duration = 2

    def resolve(self):
        self.opponent.take_damage(self.calculate_damage())
        self.contestant.reduce_energy(15)

    def calculate_damage(self):
        base_dmg = self.contestant.stats.offensive_power * random.uniform(0.5, 5)
        base_dmg += random.uniform(0.5, 1.5) * self.contestant.weapon
        base_dmg -= random.uniform(0.5, 1.5) * self.opponent.armor

        return max(0, base_dmg)
