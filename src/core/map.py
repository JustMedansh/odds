import math
from typing import TYPE_CHECKING, Any
from dataclasses import dataclass
from enum import Enum, auto
import random

if TYPE_CHECKING:
    from src.contestants.contestant import Contestant

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