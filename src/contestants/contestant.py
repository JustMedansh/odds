from __future__ import annotations

from dataclasses import dataclass, field
import random
from src.logger import Logger
from src.systems.decisions import make_decision_base, make_decision_fight
from src.actions.choices import ActionChoice
from src.core.map import Position, WorldMap

@dataclass
class Stats:
    strength: float
    intelligence: float
    social: float
    perception: float = field(init=False)
    agility: float = field(init=False)
    survivability: float = field(init=False)
    agility: float = field(init=False)

    def __post_init__(self):
        self.perception = (self.intelligence * 0.8) + (self.social * 0.2)
        self.agility = (self.intelligence * 0.6) + (self.strength * 0.4)
        self.survivability = (self.intelligence + self.strength) * 0.2
        self.agility = (self.intelligence * 0.7) + (self.strength * 0.3) 

class Contestant:
    def __init__(self, name: str, gender: str, strength: float, intelligence: float, social: float):
        self.name = name
        self.gender = gender
        self.health = 100
        self.alive = True
        self.personality = Stats(strength=strength, intelligence=intelligence, social=social)
        # Replaced with the game's shared logger when added to its contestant group.
        self.logger = Logger()
        self.position = Position(0, 0) # temp values

        self.armor: float = 0.0
        self.weapon: float = 0.0

        self.allies = []
        self.enemies = []

        self.damage_multiplier = 1
        self.health_multiplier = 1

        self.busy = False

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.name}: {self.health}"

    def move_random_dir(self):
        if self.busy:
            return
        y = self.position.y + random.uniform(2, -2)
        x = self.position.x + random.uniform(2, -2)
        self.position = Position(x, y)

    def take_damage(self, dmg: int) -> bool:
        """Simulate taking damage"""
        self.health -= dmg
        self.logger.dmg(self, dmg)
        
        if self.health <= 0:
            self.kill()

        return self.alive

    def kill(self) -> None:
        """Kill the contestant"""
        self.logger.death(self)
        self.alive = False
        self.health = 0
    
    def heal(self, amt: int) -> None:
        """Heal the contestant by given amount"""
        if not self.alive:
            return

        self.health = min(100, self.health + amt)
        self.logger.heal(self, amt)

    def get_decision_fight(self, opponent: Contestant) -> ActionChoice.Fight:
        # FLEE: 30% chance of failing, but the fight ends. Else, full damage to contestant and third of original damage to opponent
        # ATTACK: Proceed wiht normal attack
        # DEFEND: Oncoming damage is reduced by a random amount between 0 to 80, but no damage is incurred by opponent 
        # DODGE: 50% chance of failing (increases with intelligence (major) and strength (minor)) but no damage is incurred

        chose = make_decision_fight(self)
        self.logger.chose(self, chose.name)
        return chose

    def get_decision_base(self, players_in_radius) -> ActionChoice.Base:
        # return make_decision_base(self, players_in_radius)
        return ActionChoice.Base.FIGHT, players_in_radius

def random_contestant(count: int) -> list[Contestant]:
    MALE_NAMES = [
        "Aaron", "Adrian", "Aiden", "Alexander", "Andrew",
        "Anthony", "Arthur", "Benjamin", "Blake", "Caleb",
        "Cameron", "Charles", "Christopher", "Daniel", "David",
        "Dominic", "Dylan", "Ethan", "Felix", "Finn",
        "Gabriel", "Henry", "Hunter", "Isaac", "Jack",
        "Jacob", "James", "Jason", "Joshua", "Julian",
        "Kai", "Leo", "Liam", "Logan", "Lucas",
        "Marcus", "Mason", "Matthew", "Nathan", "Nicholas",
        "Noah", "Oliver", "Owen", "Parker", "Ryan",
        "Samuel", "Sebastian", "Thomas", "Victor", "William"
    ]

    FEMALE_NAMES = [
        "Abigail", "Alice", "Amelia", "Anna", "Aria",
        "Avery", "Bella", "Charlotte", "Chloe", "Claire",
        "Ella", "Emily", "Emma", "Eva", "Grace",
        "Hannah", "Harper", "Hazel", "Isabella", "Julia",
        "Layla", "Leah", "Lily", "Lucy", "Madison",
        "Maya", "Mia", "Natalie", "Nora", "Olivia",
        "Paisley", "Penelope", "Quinn", "Riley", "Rose",
        "Ruby", "Samantha", "Sarah", "Scarlett", "Skylar",
        "Sophia", "Stella", "Taylor", "Victoria", "Violet",
        "Willow", "Zoe", "Aurora", "Brooklyn", "Savannah"
    ]

    tributes = []
    for _ in range(count):
        random.shuffle(MALE_NAMES)
        random.shuffle(FEMALE_NAMES)
        gender = random.choice(['M', 'F'])

        if gender == 'M':
            name = MALE_NAMES[-1]
            MALE_NAMES.pop()

        else:
            name = FEMALE_NAMES[-1]
            FEMALE_NAMES.pop()

        skills = [random.randint(1, 10) for _ in range(3)]
        tributes.append(Contestant(name, gender, skills[0], skills[1], skills[2]))

    return tributes
