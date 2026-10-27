from tribute import get_skills
import random
from .event import Event

class Fight(Event):
    def fight(self):
        logger = self.logger
        game = self.game
        weights = {
            "strength": 3,
            "intelligence": 1,
            "random": 15,
            "weapon": 3, 
        }

        tribute_a, tribute_b = game.random_group(2)
        logger.fighting(tribute_a, tribute_b)

        while True:
            power_a, power_b = self.get_power(tribute_a, weights), self.get_power(tribute_b, weights)
            damage = self.calculate_damage(power_a, power_b)

            if power_a > power_b:
                if self.attack(tribute_a, tribute_b, damage - tribute_b.armor):
                    return tribute_a, tribute_b
                
            elif power_b > power_a:
                if self.attack(tribute_b, tribute_a, damage - tribute_a.armor):
                    return tribute_a, tribute_b
                
            else:
                self.attack_when_tie(tribute_a, tribute_b, damage)

            if self.check_death(tribute_a, tribute_b):
                return tribute_a, tribute_b

    def calculate_damage(self, power_a, power_b):
        random_value = 10
        difference = abs(power_a - power_b)
        base_damage = 15
        return (
             base_damage +
             difference +
             random.randint(-random_value, random_value)
        )

    def check_death(self, t1, t2):
        logger = self.logger
        if t1.alive and t2.alive:
            return False

        if not t1.alive:
            logger.death(t1)
        if not t2.alive:
            logger.death(t2)

        return True

    def attack(self, winner, loser, dmg):
        """
        Returns True if loser runs away, else False
        """
        self.logger.hit(loser, winner)
        loser.take_damage(dmg)
        if random.random() < 0.1:
            self.logger.run_away(loser)
            return True
        return False

    def attack_when_tie(self, t1, t2, dmg):
        damage = dmg // 2
        self.logger.dmg_both(t1, t2)
        t1.take_damage(damage)
        t2.take_damage(damage)

# class CombatEntity:
#     def __init__(self, members):
#         return members[0]