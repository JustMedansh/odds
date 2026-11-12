import math
from typing import TYPE_CHECKING, Any
from dataclasses import dataclass
from enum import Enum, auto
import random

if TYPE_CHECKING:
    from src.contestants.contestant import Contestant
    from src.contestants.grouped_contestant import GroupedContestants

@dataclass
class Position:
    x: float
    y: float

@dataclass
class Tile:
    x: int
    y: int
    terrain: Terrain

class Terrain(Enum):
    GRASS = (True, 1.0)
    WATER = (False, float("inf"))
    FOREST = (True, 1.5)
    ROCK = (True, 2.0)

class WorldMap:
    def __init__(self, height, width):
        self.positions = {}
        self.tiles = self.generate_map(height, width)
        self.height = height
        self.width = width

    def __str__(self):
        lines = []

        for position, tile in self.tiles.items():
            terrain = tile.terrain
            x, y = position
            lines.append(f"({x}, {y}): {terrain}") 

        return "\n".join(lines)

    # ---POSITION---
    def get_position(self, entity: Any):
        return self.positions.get(entity)
        
    def update_position(self, entity: Any, pos: Position):
        self.positions[entity] = pos

    # ---
    
    # ---TILES---
    def get_tile(self, pos: Position):
        return self.tiles.get(self.floor_position(pos))

    def set_tile(self, pos: Position, tile: Tile):
        self.tiles[self.floor_position(pos)] = tile

    # ---

    def generate_map(self, height: int, width: int):
        tiles = {}
        for y in range(height):
            for x in range(width):
                tiles[(x, y)] = Tile(x, y, Terrain.GRASS)

        return tiles

    def floor_position(self, pos: Position):
        return (
            math.floor(pos.x),
            math.floor(pos.y)
        )

    def get_random_position(self):
        return Position(
            x = random.uniform(0, self.width),
            y = random.uniform(0, self.height)
        )

    def get_distance(self, p1: Position, p2: Position):
        """Get distance between two points"""
        x1, y1 = p1.x, p1.y
        x2, y2 = p2.x, p2.y

        difference_x = (x1 - x2) ** 2
        difference_y = (y1 - y2) ** 2
        return math.sqrt(difference_x + difference_y)

    def get_contestants_in_radius(self, c: Contestant, r: int, gc: GroupedContestants):
        """Get all contestants in radius r"""
        players_in_radius = [p for p in gc.get_alive_contestants() 
                            if (self.get_distance(c.position, p.position) <= r)
                            and (p != c)]
        
        return players_in_radius