from tribute import Tribute
from logger import Logger 
import random

class Game:
    def __init__(self):
        self.tributes = {}
        self.day = 1
        self.next_id = 1
        self.logger = Logger()

    def add_tributes(self, tributes):
        for tribute in tributes:
            tribute.logger = self.logger
            self.tributes[self.next_id] = tribute
            self.next_id += 1
            
    def get_tribute(self, id):
        return self.tributes[id]
    
    def get_all_tributes(self):
        return self.tributes
    
    def alive_tributes(self):
        return [t for t in self.tributes.values() if t.alive]

    def dead_tributes(self):
        return [t for t in self.tributes.values() if not t.alive]
    
    def random_tribute(self):
        return random.choice(self.alive_tributes())
    
    def random_group(self, number_of_tributes):
        return random.sample(self.alive_tributes(), k=number_of_tributes)
    
    def count_dead(self):
        return len(self.dead_tributes())
    
    def count_alive(self):
        return len(self.alive_tributes())
        
