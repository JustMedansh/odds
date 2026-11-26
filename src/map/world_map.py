import numpy as np
from enum import Enum
from dataclasses import dataclass
from math import floor
from typing import Any
import random

class TerrainTypes(Enum):
    """Represents a type of terrain on a tile"""
    # TYPE = int
    # maybe later: TYPE = (walking cost, movable)
    GRASSLAND = 0
    FOREST = 1
    WATER = 2

@dataclass(frozen=True)
class Position:
    x: float
    y: float 

    @property
    def floored(self) -> tuple[int, int]:
        """A tuple communicating the location of the tile which this Position refers to, i.e floored values of x and y"""
        return (floor(self.x), floor(self.y))

    @property
    def coordinates(self) -> tuple[float, float]:
        """A tuple communicating the location of the tile as is, i.e actual values of x and y"""
        return (self.x, self.y)

class WorldMap:
    """
    Represents a world map for the simulation. Brief description:
    1. get/set_terrain is used to interact with the type of terrain at (x, y)
    2. get/set_position is used to record positions of objects (i.e contestants, loot) in the map (use Position class)

    Tiles will always be at integer location (int, int) but objects will be at float locations (float, float)
    """
    def __init__(self, width: int = 64, height: int = 64):
        """Create an instance of world-map. By default 64x64."""
        if width <= 0 or height <= 0:
            raise ValueError("Map dimensions must be positive")
        
        self.width = width
        self.height = height
        self.terrain_map = np.zeros((height, width), dtype=np.uint8)

        self.object_positions: dict[Any, Position] = {}

    def _validate_position_class(self, pos: Position) -> None:
        if not self.is_valid_position(pos):
            raise IndexError("Position outside map boundaries")    

    def is_valid_position(self, pos: Position) -> bool:
        x, y = pos.coordinates
        return (0 <= x < self.width and 0 <= y < self.height)

    # --- TERRAIN METHODS ---
    def get_terrain(self, pos: Position) -> TerrainTypes:
        """Get the type of terrain at (x, y)"""
        self._validate_position_class(pos)
        x, y = pos.floored
        return TerrainTypes(self.terrain_map[y, x])

    def set_terrain(self, pos: Position, terrain: TerrainTypes) -> None:
        """Set the type of terrain at (x, y)"""
        self._validate_position_class(pos)
        x, y = pos.floored
        self.terrain_map[y, x] = terrain.value

    def fill_terrain(self, terrain: TerrainTypes) -> None:
        """Fill the entire map with a single terrain type"""
        self.terrain_map.fill(terrain.value)

    # --- POSITION METHODS ---
    def get_position_of_object(self, obj: Any) -> Position:
        """Get the location of object"""
        position = self.object_positions[obj]
        return position

    def get_all_objects(self) -> list[tuple[Any, Position]]:
        """Return a list of all objects and their positions on the map."""
        return [tuple(i) for i in self.object_positions.items()]
    
    def set_position(self, obj: Any, position: Position) -> None:
        """Set the type of terrain at Position"""
        self._validate_position_class(position)
        self.object_positions[obj] = position

    def remove_position(self, obj: Any) -> None:
        """Remove the object from positions"""
        del self.object_positions[obj]

    def get_random_position(self) -> Position:
        """Generate a random valid world position."""
        return Position(
            random.random() * self.width,
            random.random() * self.height
        )

    def get_objects_in_radius(self, position: Position, radius: float, exclude: Any = None) -> list[tuple[Any, Position]]:
        """Return a list of objects in a radius circle from the position"""
        self._validate_position_class(position)
        valid_objects = [
            (obj, obj_pos) for obj, obj_pos in self.get_all_objects()
            if self.get_distance(position, obj_pos) <= radius and
            obj is not exclude
        ]

        return valid_objects

    @staticmethod
    def get_distance(pos1: Position, pos2: Position) -> float:
        """Get the distance between two positions"""
        x1, y1 = pos1.coordinates
        x2, y2 = pos2.coordinates

        sq_difference_x = (x1 - x2) ** 2
        sq_difference_y = (y1 - y2) ** 2

        return (sq_difference_x + sq_difference_y) ** 0.5
    
    # --- TILE METHODS ---
    def get_objects_at(self, position: Position) -> list[Any]:
        """Get list of objects at certain tile"""
        self._validate_position_class(position)
        return [obj for obj, obj_pos in self.object_positions.items() if obj_pos.floored == position.floored]
    
    def get_neighbours(self, position: Position, radius: int = 1) -> list[Position]:
        """Return valid neighbours of a position in a square radius"""
        if radius < 0:
            raise ValueError("Radius cannot be negative")

        self._validate_position_class(position)

        neighbours = []
        x, y = position.floored

        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                neighbour = Position(x + dx, y + dy)
                if self.is_valid_position(neighbour) and (dx, dy) != (0, 0):
                    neighbours.append(neighbour)

        return neighbours    

    def get_random_tile_position(self) -> Position:
        x, y = self.get_random_position().floored
        return Position(x, y)
