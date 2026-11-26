from __future__ import annotations
from .profile.attributes import Stats, Personality, Skills
from dataclasses import dataclass, field
from src.map.world_map import Position
import random

@dataclass
class Contestant:
    """Representation of a contestant"""
    name: str
    gender: str
    stats: Stats
    personality: Personality = field(default_factory=Personality)
    skills: Skills = field(default_factory=Skills)

    health: float = 100
    energy: float = 100

    position: Position = Position(0, 0)

    armor: float = 0.0
    weapon: float = 0.0

    active_actions: list = field(default_factory=list)

    @property
    def alive(self) -> bool:
        return self.health > 0

    def set_position(self, new_pos: Position) -> None:
        """Set the position of the current contestant"""
        self.position = new_pos

    def __str__(self):
        return f"{self.name}: {self.health}"

    def take_damage(self, dmg: int) -> None:
        """Reduce health by given amount"""
        if dmg < 0:
            raise ValueError("Damage cannot be negative")
        
        self.health = max(0, self.health - dmg)
    
    def heal(self, amt: int) -> None:
        """Heal the contestant by given amount"""
        if amt < 0:
            raise ValueError("Healing cannot be negative")
        
        if not self.alive:
            return

        self.health = min(100, self.health + amt)

    def reduce_energy(self, amt: int) -> None:
        """Reduce energy by given amount"""
        if amt < 0:
            raise ValueError("Reduction cannot be negative")
        
        self.energy = max(0, self.energy - amt)
        
    def add_energy(self, amt: int) -> None:
        """Add energy to the contestant by given amount"""
        if amt < 0:
            raise ValueError("Addition cannot be negative")
        
        if not self.alive:
            return

        self.energy = min(100, self.energy + amt)

def random_contestant(k: int) -> list[Contestant]:
    """Get k contestants with randomized values, max 50 (temp.)"""

    if not 1 <= k <= 50:
        raise ValueError("Contestant count must be between 1 and 50")

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

    contestants = []
    random.shuffle(MALE_NAMES)
    random.shuffle(FEMALE_NAMES)
    
    for _ in range(k):
        gender = random.choice(['M', 'F'])

        if gender == 'M':
            name = MALE_NAMES[-1]
            MALE_NAMES.pop()

        else:
            name = FEMALE_NAMES[-1]
            FEMALE_NAMES.pop()

        skills = [random.randint(1, 10) for _ in range(3)]
        stats = Stats(skills[0], skills[1], skills[2])
        contestants.append(Contestant(name, gender, stats))

    return contestants
