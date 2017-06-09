from src.map.master_color_map import MasterColorMap
from src.map.tile_map import TileMap
from src.image.map_image import MapImage


class MasterMap(object):

    def __init__(self):

        self.terrain_map = None
        self.tile_map = None
        self.color_map = None  # MasterColorMap(self.terrain_map)

        self.map_image = None

    def set_terrain_map(self, terrain_map):
        self.terrain_map = terrain_map

    def initialize(self):

        self.tile_map = TileMap(self.terrain_map)
        self.tile_map.initialize()

        self.color_map = MasterColorMap(self.terrain_map)

        self.map_image = MapImage(self)

    @property
    def w(self):
        return self.terrain_map.w

    @property
    def h(self):
        return self.terrain_map.h
