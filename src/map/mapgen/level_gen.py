from map_generator import MapGen
from src.map.level import Level
from src.map.tile_map import TileMap
from src.map.master_color_map import MasterColorMap
from src.image.map_image import MapImage

from random import *


class LevelGen(object):

    @classmethod
    def generate_level(cls, game_state, map_seed=None):

        if map_seed is None:
            map_seed = randint(0, 9999)
        seed(map_seed)

        level = Level(game_state, map_seed=map_seed)
        terrain = MapGen.generate_terrain_map_cave(45, 25, map_seed=map_seed)

        cls.initialize_level(level, terrain)

        cls.initialize_color_sources(level)
        cls.create_door_objects(level)

        level.set_map_image(MapImage(level))

        return level

    @classmethod
    def initialize_level(cls, level, terrain):

        level.set_terrain_map(terrain)

        level.tile_map = TileMap(level.terrain_map)
        level.tile_map.initialize()

        level.color_map = MasterColorMap(level)
        level.color_source_generator.set_color_map(level.color_map)

    @classmethod
    def initialize_color_sources(cls, level):

        crystals = filter(lambda x: level.terrain_map.get_tile_id(x) == 'large_crystal', level.terrain_map.all_points)

        for point in crystals:
            color = choice(('red', 'green', 'blue'))
            level.map_object_generator.add_crystal(point, color)
            #level.color_source_generator.get_color_source(point, color, 5)

    @classmethod
    def create_door_objects(cls, level):

        doors = filter(lambda x: level.terrain_map.get_tile_id(x) == 'door', level.terrain_map.all_points)

        for point in doors:
            level.map_object_generator.add_door(point)
