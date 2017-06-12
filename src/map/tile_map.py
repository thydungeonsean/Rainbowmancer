from _map import _Map
from random import *


class TileMap(_Map):
    
    key = {
        0: 'blank',
        1: 'tuft_1',
        2: 'tuft_2',
        3: 'tuft_3',
        4: 'tuft_4',
        5: 'grass_1',
        6: 'grass_2',
        7: 'stone_1',
        8: 'stone_2',
        9: 'stone_3',
        10: 'dungeon_ver_wall',
        11: 'dungeon_hor_wall_1',
        12: 'dungeon_hor_wall_2',
        13: 'cavern_ver_wall',
        14: 'cavern_hor_wall_1',
        15: 'cavern_hor_wall_2',
        16: 'door_closed',
        17: 'door_opened',
        18: 'stairs_down',
        20: 'brazier_off',
        21: 'brazier_lit_ani',
        30: 'crystal_large',
        32: 'crystal_small',
        34: 'stalagtite_1',
        35: 'stalagtite_2',
    }

    encode = {v: k for (k, v) in key.iteritems()}
    
    def __init__(self, terrain_map):
        
        w = terrain_map.w
        h = terrain_map.h
        self.map_seed = terrain_map.map_seed
        _Map.__init__(self, w, h)
        self.terrain_map = terrain_map
        
    def point_is_animated(self, point):
        return self.get_tile_key(point).endswith('ani')
        
    def get_tile_key(self, point):
        return TileMap.key[self.get_tile(point)]
        
    def initialize(self):
        # translate terrain_map tile data into specific tile keys
        seed(self.map_seed)
        for point in self.all_points:

            tile_id = self.terrain_map.get_tile_id(point)
            if tile_id == 'floor':
                self.set_floor_tile(point)
            elif tile_id == 'wall':
                self.set_wall_tile(point)
            elif tile_id == 'door':
                self.set_door_tile(point)
            elif tile_id == 'brazier':
                self.set_brazier_tile(point)
            elif tile_id == 'stalagtite':
                self.set_stalagtite_tile(point)
            elif tile_id == 'large_crystal':
                self.set_large_crystal_tile(point)
            elif tile_id == 'small_crystal':
                self.set_small_crystal_tile(point)
            elif tile_id == 'stairs':
                self.set_stairs_tile(point)

    def set_floor_tile(self, point):
        if randint(0, 99) < 65:
            t = 0
        else:
            t = choice(range(1, 10))
        self.set_tile(t, point)

    def set_wall_tile(self, (px, py)):

        if self.point_in_bounds((px, py+1)) and self.terrain_map.get_tile((px, py+1)) not in (1, 2):
            tile_code = choice((14, 14, 15))
        else:
            tile_code = 13

        self.set_tile(tile_code, (px, py))

    def set_door_tile(self, point):
        self.set_tile(TileMap.encode['door_closed'], point)

    def set_brazier_tile(self, point):
        self.set_tile(TileMap.encode['brazier_lit_ani'], point)

    def set_stalagtite_tile(self, point):
        self.set_tile(randint(34, 35), point)

    def set_large_crystal_tile(self, point):
        self.set_tile(TileMap.encode['crystal_large'], point)

    def set_small_crystal_tile(self, point):
        self.set_tile(TileMap.encode['crystal_small'], point)

    def set_stairs_tile(self, point):
        self.set_tile(TileMap.encode['stairs_down'], point)
