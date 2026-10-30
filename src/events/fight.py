import random
from .event import Event
from src.contestants.contestant import Contestant
from src.contestants.grouped_contestant import GroupedContestants
from src.logger import Logger

# each contestant is sent the opponent
# they can choose to FLEE, ATTACK, DEFEND, DODGE, NOTHING
# FLEE: 30% chance of failing, but the fight ends. Else, full damage to contestant and third of original damage to opponent
# ATTACK: Proceed wiht normal attack
# DEFEND: Oncoming damage is reduced by a random amount between 0 to 80, but no damage is incurred by opponent 
# DODGE: 50% chance of failing (increases with intelligence (major) and strength (minor)) but no damage is incurred

class Fight(Event):
    def reset_multipliers(self, *contestants: Contestant):
        for c in contestants:
            c.damage_multiplier = 1
            c.health_multiplier = 1

    def fight(self, c1: Contestant, c2: Contestant) -> tuple[Contestant, Contestant]:
        """Stage a fight between two random contestants"""
        logger: Logger = self.logger
        # game: GroupedContestants = self.game

        contestant_a, contestant_b = c1, c2
        logger.fighting(contestant_a, contestant_b)

        while True:
            self.reset_multipliers(contestant_a, contestant_b)
            if self.resolve_turn(contestant_a, contestant_b):
                return contestant_a, contestant_b

    def resolve_turn(self, contestant_a: Contestant, contestant_b: Contestant) -> tuple[Contestant, Contestant] | bool:
        """Resolve a single turn between two contestants"""
        weights = {
            "strength": 3,
            "intelligence": 1,
            "random": 15,
            "weapon": 3,
        }

        fight_dispatcher = {
            'FLEE': self.flee_handler,
            'ATTACK': self.attack_handler,
            'DEFEND': self.defend_handler,
            'DODGE': self.dodge_handler
        }

        choice_a = contestant_a.make_decision_fight(contestant_b)
        choice_b = contestant_b.make_decision_fight(contestant_a)

        result_a = fight_dispatcher[choice_a](contestant_a)
        result_b = fight_dispatcher[choice_b](contestant_b)

        resolve_hit_a = (choice_a == 'ATTACK')
        resolve_hit_b = (choice_b == 'ATTACK')

        if not result_a or not result_b:
            return contestant_a, contestant_b

        if resolve_hit_a:
            if self.resolve_hit(contestant_a, contestant_b, weights):
                return contestant_a, contestant_b

        if resolve_hit_b:
            if self.resolve_hit(contestant_b, contestant_a, weights):
                return contestant_a, contestant_b

        return False

    def resolve_hit(self, contestant_a: Contestant, contestant_b: Contestant, weights: dict):
        power_a = self.get_power(contestant_a, weights)
        power_b = self.get_power(contestant_b, weights)
        damage = self.calculate_damage(power_a, power_b)

        total_damage = (damage - contestant_b.armor) * contestant_a.damage_multiplier * contestant_b.health_multiplier
        if power_a < power_b - random.randint(0, 15):
            total_damage //= 3

        total_damage = round(total_damage)

        if self.attack(
            contestant_a,
            contestant_b,
            total_damage,
        ):
            return contestant_a, contestant_b

        if self.check_death(contestant_a, contestant_b):
            return contestant_a, contestant_b
                    
        return False

    def defend_handler(self, c: Contestant):
        c.damage_multiplier = 0.2
        c.health_multiplier = float(random.randint(5, 8) / 10)
        return True # to ensure flee works

    def attack_handler(self, c: Contestant):
        return True

    def dodge_handler(self, c: Contestant):
        c.damage_multiplier = 0.2
        dodge_chance = random.random()
        if dodge_chance < 0.5:
            c.health_multiplier = 0

        return True

    def flee_handler(self, c: Contestant):
        c.damage_multiplier = 0.2
        flee_chance = random.random()
        if flee_chance < 0.8:
            self.logger.run_away(c)
            return False
        return True
    
    def calculate_damage(self, power_a: int, power_b: int) -> int:
        """Calculate damage taken by the weaker contestant"""
        random_value = 10
        difference = abs(power_a - power_b)
        base_damage = 15

        return (
            base_damage
            + difference
            + random.randint(-random_value, random_value)
        )

    def check_death(self, contestant_a: Contestant, contestant_b: Contestant) -> bool:
        """Return True if either contestant dies."""
        if contestant_a.alive and contestant_b.alive:
            return False

        return True

    def attack(self, attacker: Contestant, target: Contestant, damage: int) -> bool:
        """Returns True if the target runs away, otherwise False."""
        damage = max(0, damage)

        if damage != 0:
            self.logger.hit(target, attacker)
        target.take_damage(damage)

        return False

# class CombatEntity:
#     """A class managing combat for a contestant or group of contestants"""
#     def __init__(self, contestants: list[Contestant]) -> None:
#         pass

#     @staticmethod
#     def get_power(contestant: Contestant, weights: dict[str, int]):
#         """Calculate power with randomness and stats"""
#         power = 0
#         for stat, weight in weights.items():
#             if stat == "random":
#                 continue

#             if stat in contestant.skills:
#                 value = contestant.skills[stat]
#             else:
#                 value = getattr(contestant, stat)

#             power += value * weight 

#         power += random.randint(-weights['random'], weights['random'])
#         return power
