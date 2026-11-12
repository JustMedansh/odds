# import pytest
# from src.core.map import WorldMap, Position, Tile, Terrain

# @pytest.fixture
# def world():
#     return WorldMap(5, 5)

# def test_map_generation(world):
#     assert len(world.tiles) == 25

# def test_tile_coordinates_match_keys(world):
#     for (x, y), tile in world.tiles.items():
#         assert tile.x == x
#         assert tile.y == y

# def test_get_tile(world):
#     tile = world.get_tile(Position(0, 0))

#     assert tile is not None
#     assert tile.terrain == Terrain.GRASS

# def test_fractional_position(world):
#     tile = world.get_tile(Position(2.7, 3.4))

#     assert tile is not None
#     assert (tile.x, tile.y) == (2, 3)

# def test_negative_position_floors_correctly(world):
#     assert world.floor_position(Position(-0.5, -1.7)) == (-1, -2)

# def test_out_of_bounds_position(world):
#     assert world.get_tile(Position(5, 5)) is None

# def test_set_tile(world):
#     new_tile = Tile(2, 2, Terrain.FOREST)
#     world.set_tile(Position(2, 2), new_tile)
#     assert world.get_tile(Position(2, 2)).terrain == Terrain.FOREST

# def test_entity_location_update(world):
#     entity = object()
#     position = Position(2.5, 3.5)
#     world.update_location(entity, position)
#     assert world.positions[entity] == position

# def test_all_generated_tiles_are_grass(world):
#     for tile in world.tiles.values():
#         assert tile.terrain == Terrain.GRASS