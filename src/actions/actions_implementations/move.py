from __future__ import annotations

import math
from typing import TYPE_CHECKING

from ..actions_base import Action
from src.map.world_map import Position

if TYPE_CHECKING:
    from src.contestants import Contestant

class Move(Action):
    def __init__(self, contestant: Contestant, direction: float, speed: float = 1):
        super().__init__(contestant)
        self.duration = None
        self.direction = direction % 360
        self.speed = speed

        if not 0 < speed <= 2:
            raise ValueError(f"Speed cannot be above 2 or below zero, current {speed}")

    def on_tick(self):
        x, y = self.contestant.position.coordinates
        radians = math.radians(self.direction)

        dx = math.cos(radians) * self.speed
        dy = math.sin(radians) * self.speed

        new_pos = Position(x + dx, y + dy)
        self.contestant.set_position(new_pos)
        self.contestant.reduce_energy(0.5 * self.speed)

    def resolve(self):
        pass
