import random
from src.logger import Logger

SKILLS = {
    'strength': 0,
    'intelligence': 0,
    'social': 0,
}

class Contestant:
    def __init__(self, name: str, gender: str, skills=None):
        self.name = name
        self.gender = gender
        self.health = 100
        self.alive = True
        self.alliance = []
        self.enemies = []
        self.skills = skills.copy() if skills is not None else SKILLS.copy()
        self.logger = Logger()

        self.armor = 0
        self.weapon = 0

    def __str__(self):
        attrs = []
        for name, value in self.__dict__.items():
            attrs.append(f"{name}: {value}")

        return f"{"\n".join(attrs)}\n"

    def __repr__(self):
        return f"{self.name}: {self.health}"

    def take_damage(self, dmg: int) -> bool:
        """Simulate taking damage"""
        self.health -= dmg
        if self.health <= 0:
            self.kill()

        self.logger.dmg(self, dmg)
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

        skills = {
            skill: random.randint(1, 10) for skill in SKILLS
        }

        tributes.append(Contestant(name, gender, skills))

    return tributes

def get_skills():
    return SKILLS