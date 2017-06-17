from src.map.master_color_map import MasterColorMap
from src.map.tile_map import TileMap
from src.image.map_image import MapImage
from color_source import ColorSourceGen
from map_object_generator import MapObjectGen
from redraw_manager import RedrawManager
from fov_map import FOVMap


class Level(object):

    def __init__(self, game_state, map_seed=None):

        self.map_seed = map_seed

        self.game = game_state

        self.terrain_map = None
        self.tile_map = None
        self.color_map = None  # MasterColorMap(self.terrain_map)

        self.fov_map = FOVMap(self)

        self.map_image = None

        self.player_start = (0, 0)

        self.color_source_generator = ColorSourceGen()
        self.map_object_generator = MapObjectGen(self)

        self.redraw_manager = RedrawManager(self)

    def load_game(self, game):
        self.game = game

    def load_player(self, player):
        self.fov_map.set_player(player)
        self.fov_map.recompute_fov()

    def set_terrain_map(self, terrain_map):
        self.terrain_map = terrain_map
        self.player_start = self.terrain_map.entrance

    def set_map_image(self, map_image):
        self.map_image = map_image

    @property
    def w(self):
        return self.terrain_map.w

    @property
    def h(self):
        return self.terrain_map.h
