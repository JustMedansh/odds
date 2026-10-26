class Contestant:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.dead = False

    def take_damage(self, amount):
        self.health = max(self.health - amount, 0)
        if self.health == 0:
            self.dead = True

    def __repr__(self):
        return f"{self.name}: {self.health}"

    def is_dead(self):
        return self.dead

class GroupedContestants:
    # t -> contestant
    # cs -> contestants

    def __init__(self):
        self.cs = []

    def add(self, contestants):
        for contestant in contestants:
            self.cs.append(contestant)

    def get_dead(self):
        return [t for t in self.cs if t.is_dead()]

    def get_living(self):
        return [t for t in self.cs if not t.is_dead()]

    def __str__(self):
        return str(self.cs)