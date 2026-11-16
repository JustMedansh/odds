from __future__ import annotations
from dataclasses import dataclass
import random
from typing import TYPE_CHECKING

from ..action_base import ActionBase
from ..choices import ActionChoice
from encounter import Encounter
from src.logger import Logger

if TYPE_CHECKING:
    from src.contestants.contestant import Contestant
    from src.core.game import Game

# Combat should work in a way that you can pass in an Encounter and call update 
# to advance a stage

class Combat(ActionBase):
    """Simulate a single fight round."""
    def __init__(self, encounter: Encounter):
        self.encounter = encounter
        self.multipliers = {}
        self.logger = Logger()

    def reset_multipliers(self, *contestants: Contestant):
        """Reset the multipliers dictionary"""
        self.multipliers = {}

    @staticmethod
    def get_dodge_status(contestant: Contestant):
        """Return health multiplier 0.0, 1.0, or 0.5 according to the agility of the contestant """
        agility = contestant.personality.agility / 10
        return random.choices([0.0, 0.5, 1.0], [1 - agility, 0.5, agility])[0]

    def get_multiplier(self, decision: ActionChoice.Combat, contestant: Contestant):
        """Get the multiplier values for each decision"""
        # (offensive_multiplier, defensive_multiplier)
        multiplier_dispatch = {
            ActionChoice.Combat.Offensive.ATTACK: (1.0, random.uniform(0.7, 0.9)),

            ActionChoice.Combat.Defensive.DEFEND: (0.2, random.uniform(0.2, 0.4)),
            ActionChoice.Combat.Defensive.DODGE: (0.0, self.get_dodge_status(contestant)),

            ActionChoice.Combat.GameEnding.FLEE: (0.0, 0.0)
        }

        return multiplier_dispatch[decision]

    def calculate_multipliers(self, choices: dict[Contestant, CombatDecision]):
        """Get decision from each player and store in multipliers"""
        multipliers = {}
        for contestant, choice in choices.items():
            multipliers[contestant] = self.get_multiplier(choice.action, contestant)

        return multipliers

    @staticmethod
    def get_decisions(contestants: list[Contestant]) -> dict[Contestant, CombatDecision]:
        """Get a decision from each contestant"""
        choices = {}
        for contestant in contestants:
            choice = contestant.get_decision_combat([t for t in contestants if t != contestant])
            choices[contestant] = choice

        return choices

    def stage(self, contestants: list[Contestant]) -> bool:
        """Advance this combat by one game tick; return whether it is still active."""
        choices = self.get_decisions(contestants)
        multipliers = self.calculate_multipliers(choices)
        damages = self.calculate_damages(choices, multipliers)
        self.apply_damages(damages)

    def apply_damages(self, damages: dict[Contestant, float]):
        for c, d in damages.items():
            c.take_damage(d)

    def flee_handler(self, c: Contestant):
        pass

    @staticmethod
    def get_attackers(choices: dict[Contestant, CombatDecision], contestant: Contestant):
        attackers = []
        for c, choice in choices.items():
            if choice.action == ActionChoice.Combat.Offensive and choice.opponent == contestant:
                attackers.append(c)

        return attackers
    
    def calculate_damages(self, choices: dict[Contestant, CombatDecision], multipliers: dict[Contestant, tuple[float, float]]) -> dict[Contestant, float]:
        """Calculate damage taken by the each contestant"""
        damages = {}

        for c in self.encounter.get_all_contestants():
            attackers = self.get_attackers(choices, c)
            power = self.get_total_power([c])
            difference = sum([(self.get_total_power(a) - power) * multipliers[a][0] for a in attackers])

            RANDOM_VALUE = 10
            BASE_DAMAGE = 15

            damage_taken = min(
                ((
                    BASE_DAMAGE
                    + difference
                    + random.randint(-RANDOM_VALUE, RANDOM_VALUE)
                ) * multipliers[c][1]),

                5
            )

            damages[c] = damage_taken

        return damages


    def get_total_power(self, contestants: list[Contestant]):
        weights = {
            "strength": 3,
            "intelligence": 1,
            "random": 15,
            "weapon": 3,
        }

        power = 0

        for c in contestants:
            power += self.get_power(c, weights)

        return power ** 0.8

    def check_death(self, contestant_a: Contestant, contestant_b: Contestant) -> bool:
        """Return True if either contestant dies."""
        pass

@dataclass
class CombatDecision: 
    action: ActionChoice.Combat
    opponent: Contestant | None
