from __future__ import annotations
from .tags import StatTags, get_attribute_value
from dataclasses import dataclass, field
import random

@dataclass
class Stats:
    strength: float | StatTags.Attribute.Strength
    intelligence: float | StatTags.Attribute.Intelligence
    social: float | StatTags.Attribute.Social
    perception: float = field(init=False)
    agility: float = field(init=False)
    survivability: float = field(init=False)

    def __post_init__(self):
        # Attributes
        if isinstance(self.strength, StatTags.Attribute.Strength):
            self.strength = get_attribute_value(self.strength)

        if isinstance(self.intelligence, StatTags.Attribute.Intelligence):
            self.intelligence = get_attribute_value(self.intelligence)

        if isinstance(self.social, StatTags.Attribute.Social):
            self.social = get_attribute_value(self.social)

        # Specialized
        self.perception = (self.intelligence * 0.8) + (self.social * 0.2)
        self.survivability = (self.intelligence + self.strength) * 0.2
        self.agility = (self.intelligence * 0.7) + (self.strength * 0.3) 

@dataclass
class Contestant:
    name: str
    gender: str
    stats: Stats

    alive: bool = True
    health: int = 100

    armor: float = 0.0
    weapon: float = 0.0

    def __str__(self):
        return f"{self.name}: {self.health}"

    def take_damage(self, dmg: int) -> None:
        """Reduce health by given amount"""
        self.health -= dmg
    
        if self.health <= 0:
            self.alive = False
            self.health = 0
    
    def heal(self, amt: int) -> None:
        """Heal the contestant by given amount"""
        if not self.alive:
            return

        self.health = min(100, self.health + amt)

def random_contestant(k: int) -> list[Contestant]:
    """Get k contestants with randomized values"""

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