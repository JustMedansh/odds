from random import shuffle, randint
from logger import Logger

SKILLS = {
    'strength': 0,
    'intelligence': 0
}

class Tribute:
    def __init__(self, name, gender, skills=SKILLS):
        """
        Initializes a tribute object
        """
        self.name = name
        self.gender = gender
        self.health = 100
        self.alive = True
        self.alliance = []
        self.enemies = []
        self.skills = skills

        self.armor = 0
        self.weapon = 0

    def __str__(self):
        attrs = []
        for name, value in self.__dict__.items():
            attrs.append(f"{name}: {value}")

        return f"{"\n".join(attrs)}\n"

    def __repr__(self):
        attrs = []
        for name, value in self.__dict__.items():
            attrs.append(f"{name}: {value}")

        return "\n".join(attrs)

    def take_damage(self, dmg):
        """
        Reduces health. Returns True if the tribute survives, False otherwise.
        """
        self.health -= dmg
        if self.health <= 0:
            self.alive = False
            self.health = 0

        self.logger.dmg(self, dmg)
        return not self.alive
    
    def heal(self, amt):
        """
        Heals health by a certain amount
        """

        if not self.alive:
            return

        self.health = min(100, self.health + amt)
        self.logger.heal(self, amt)

def random_tributes(count):
#     MALE_NAMES = [
#     "Aaron", "Adrian", "Aiden", "Alexander", "Andrew",
#     "Anthony", "Arthur", "Benjamin", "Blake", "Caleb",
#     "Cameron", "Charles", "Christopher", "Daniel", "David",
#     "Dominic", "Dylan", "Ethan", "Felix", "Finn",
#     "Gabriel", "Henry", "Hunter", "Isaac", "Jack",
#     "Jacob", "James", "Jason", "Joshua", "Julian",
#     "Kai", "Leo", "Liam", "Logan", "Lucas",
#     "Marcus", "Mason", "Matthew", "Nathan", "Nicholas",
#     "Noah", "Oliver", "Owen", "Parker", "Ryan",
#     "Samuel", "Sebastian", "Thomas", "Victor", "William"
# ]

    MALE_NAMES = [
        'Medansh', 'Sahej', 'Aksh', 'Jitesh', 'Jashan', 'Abhudaya'
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
    for k in range(count):
        shuffle(MALE_NAMES)
        shuffle(FEMALE_NAMES)
        # gender = random.choice(['M', 'F'])
        gender = 'M'

        if gender == 'M':
            name = MALE_NAMES[-1]
            MALE_NAMES.pop()

        else:
            name = FEMALE_NAMES[-1]
            FEMALE_NAMES.pop()

        skills = {
            skill: randint(1, 10) for skill in SKILLS
        }

        tributes.append(Tribute(name, gender, skills))

    return tributes

def get_skills():
    return SKILLS