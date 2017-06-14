from src.map.master_color_map import MasterColorMap
from src.map.tile_map import TileMap
from src.image.map_image import MapImage
from color_source import ColorSourceGen
from map_object_generator import MapObjectGen
from redraw_manager import RedrawManager


class MasterMap(object):

    def __init__(self):

        self.game = None

        self.terrain_map = None
        self.tile_map = None
        self.color_map = None  # MasterColorMap(self.terrain_map)

        self.fov_map = None

        self.map_image = None

        self.player_start = (0, 0)

        self.color_source_generator = ColorSourceGen()
        self.map_object_generator = MapObjectGen(self)

        self.redraw_manager = RedrawManager(self)

    def load_game(self, game):
        self.game = game

    def set_terrain_map(self, terrain_map):
        self.terrain_map = terrain_map
        self.player_start = self.terrain_map.entrance

    def initialize(self):

        self.tile_map = TileMap(self.terrain_map)
        self.tile_map.initialize()

        self.color_map = MasterColorMap(self.terrain_map)
        self.color_source_generator.set_color_map(self.color_map)

        self.map_image = MapImage(self)

    @property
    def w(self):
        return self.terrain_map.w

    @property
    def h(self):
        return self.terrain_map.h
