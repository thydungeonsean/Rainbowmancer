from map_generator import MapGen
from src.map.level import Level
from src.map.tile_map import TileMap
from src.map.master_color_map import MasterColorMap
from src.image.map_image import MapImage

from random import seed, choice, sample


class LevelGen(object):

    map_seed = None

    @classmethod
    def generate_level(cls, game_state, map_seed=None):

        level = Level(1, game_state, map_seed=map_seed)
        cls.map_seed = level.map_seed
        terrain = MapGen.generate_terrain_map_cave(45, 25, map_seed=cls.map_seed)

        cls.initialize_level(level, terrain)

        cls.initialize_color_sources(level)
        cls.create_door_objects(level)

        cls.initialize_fov(level)

        cls.spawn_monsters(level, 12)

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

        seed(cls.map_seed)

        crystals = filter(lambda x: level.terrain_map.get_tile_id(x) == 'large_crystal', level.terrain_map.all_points)

        for point in crystals:
            color = choice(('red', 'green', 'blue'))
            level.map_object_generator.add_crystal(point, color)
            #level.color_source_generator.get_color_source(point, color, 5)

        level.color_map.recompute_maps()

        braziers = filter(lambda x: level.terrain_map.get_tile_id(x) == 'brazier', level.terrain_map.all_points)

        for point in braziers:
            level.map_object_generator.add_brazier(point)

    @classmethod
    def create_door_objects(cls, level):

        doors = filter(lambda x: level.terrain_map.get_tile_id(x) == 'door', level.terrain_map.all_points)

        for point in doors:
            level.map_object_generator.add_door(point)

    @classmethod
    def initialize_fov(cls, level):

        level.fov_map.init_fov_map()

    @classmethod
    def spawn_monsters(cls, level, num):

        seed(cls.map_seed)

        level.fov_map.recompute_fov(center=level.terrain_map.entrance)
        visible = level.fov_map.get_visible_points(level.terrain_map.entrance)

        floor = set(filter(lambda x: level.terrain_map.get_tile(x) == 0, level.terrain_map.all_points))

        spawn_locations = floor.difference(visible)  # all floor locations not in fov for player start

        # TODO added weigthed algorithm to space monsters better later
        monster_points = sample(spawn_locations, num)

        for point in monster_points:
            level.map_object_generator.add_random_monster(point)

