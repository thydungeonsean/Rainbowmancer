from color_source import ColorSourceGen
from map_object_generator import MapObjectGen
from redraw_manager import RedrawManager
from fov_map import FOVMap
from path_finding_map import PathFindingMap
from random import randint


class Level(object):

    def __init__(self, floor, game_state, map_seed=None):

        self.floor_number = floor

        self.map_seed = self.set_map_seed(map_seed)

        self.game = game_state

        self.terrain_map = None
        self.tile_map = None
        self.color_map = None
        self.fov_map = FOVMap(self)
        self.path_finding_map = PathFindingMap(self)

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

    def set_map_seed(self, map_seed):

        if map_seed is None:
            map_seed = randint(1, 999999999)

        map_seed = ''.join((str(map_seed), 'floor', str(self.floor_number)))
        return map_seed
