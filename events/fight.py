import random
from .event import Event
from src.contestant import Contestant
from src.game import Game
from src.logger import Logger

class Fight(Event):
    def fight(self) -> tuple[Contestant, Contestant]:
        """Stage a fight between two random contestants"""
        logger: Logger = self.logger
        game: Game = self.game

        contestant_a, contestant_b = game.random_group(2)
        logger.fighting(contestant_a, contestant_b)

        while True:
            if self.resolve_turn(contestant_a, contestant_b):
                return contestant_a, contestant_b

            if self.check_death(contestant_a, contestant_b):
                return contestant_a, contestant_b

    def resolve_turn(self, contestant_a: Contestant, contestant_b: Contestant) -> tuple[Contestant, Contestant] | bool:
        """Resolve a single turn between two contestants"""
        weights = {
            "strength": 3,
            "intelligence": 1,
            "random": 15,
            "weapon": 3,
        }

        power_a = self.get_power(contestant_a, weights)
        power_b = self.get_power(contestant_b, weights)
        damage = self.calculate_damage(power_a, power_b)

        if power_a > power_b:
            if self.attack(
                contestant_a,
                contestant_b,
                damage - contestant_b.armor,
            ):
                return contestant_a, contestant_b

        elif power_b > power_a:
            if self.attack(
                contestant_b,
                contestant_a,
                damage - contestant_a.armor,
            ):
                return contestant_a, contestant_b

        else:
            self.attack_when_tie(
                contestant_a,
                contestant_b,
                damage,
            )

        return False
    
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

        self.logger.hit(target, attacker)
        target.take_damage(damage)

        if target.alive:
            if (random.random() < 0.1) or (target.health < random.randint(10, 30) and random.random() < 0.95):
                self.logger.run_away(target)
                return True

        return False

    def attack_when_tie(self, contestant_a: Contestant, contestant_b: Contestant, damage: int) -> None:
        """Allow taking damage when powers are equal"""
        damage = max(0, damage // 2)

        self.logger.dmg_both(contestant_a, contestant_b)
        contestant_a.take_damage(damage)
        contestant_b.take_damage(damage)