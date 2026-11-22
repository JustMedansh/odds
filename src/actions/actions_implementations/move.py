import random
import math
from ..actions_base import Action, Contestant
from src.map.world_map import Position

class Move(Action):
    def __init__(self, contestant: Contestant, direction: float, speed: float = 1):
        super().__init__(contestant)
        self.duration = None
        self.direction = direction % 360
        self.speed = speed

        if not 0 < speed <= 2:
            raise ValueError(f"Speed cannot be above 2 or below zero, current {speed}")

    def update(self):
        x, y = self.contestant.position
        radians = math.radians(self.direction)

        dx = math.cos(radians) * self.speed
        dy = math.sin(radians) * self.speed

        new_pos = Position(x + dx, y + dy)
        self.contestant.set_position(new_pos)

    def resolve(self):
        pass
