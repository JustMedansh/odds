import random
from logger import Logger

class Contestant:
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
        self.health = 100
        self.dead = False
        self.logger = Logger()

    def take_damage(self, amount):
        self.health = max(self.health - amount, 0)
        self.logger.recieved_damage(self, amount)
        if self.health == 0:
            self.kill()

    def heal(self, amount):
        if not self.dead:
            self.logger.healed(self, amount)
            self.health = min(self.health + amount, 100)

    def __repr__(self):
        return f"{self.name}: {self.health}"

    def kill(self):
        if not self.is_dead():
            self.logger.death(self)
            self.health = 0
            self.dead = True

    def is_dead(self):
        return self.dead


class GroupedContestants:
    # t -> contestant
    # cs -> contestants

    def __init__(self):
        self.cs = []
        self.next_id = 0

    def __str__(self):
        return str(self.cs)
    
    def add(self, contestants):
        for contestant in contestants:
            self.cs.append(contestant)

    def add_random(self, k):
        self.cs.extend(random_tributes(k))

    def get_dead(self):
        return [t for t in self.cs if t.is_dead()]

    def get_count(self):
        return len(self.cs)

    def get_count_living(self):
        return len(self.get_living())

    def get_count_dead(self):
        return len(self.get_dead())

    def get_living(self):
        return [t for t in self.cs if not t.is_dead()]

    def get_group(self, k):
        return random.sample(self.get_living(), k)

    def get_contestant(self):
        return random.choice(self.get_living())

    def attack(self):
        attacker, defender = tuple(self.get_group(2))
        damage = 100
        Logger().hit(attacker, defender)
        defender.take_damage(damage)
        

def random_tributes(count):
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

    gc = []
    for k in range(count):
        random.shuffle(FEMALE_NAMES)
        random.shuffle(MALE_NAMES)
        gender = random.choice(['M', 'F'])

        if gender == 'M':
            name = MALE_NAMES[-1]
            MALE_NAMES.pop()

        else:
            name = FEMALE_NAMES[-1]
            FEMALE_NAMES.pop()

        gc.append(Contestant(name, gender))

    return gc
