from _map import _Map


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
    20: 'brazier_off',
    21: 'brazier_lit_ani_a',
    22: 'brazier_lit_ani_b',
    30: 'crystal_large',
    32: 'crystal_small',
    34: 'stalagtite_1',
    35: 'stalagtite_2',
    }
    
    def __init__(self, terrain_map, ani_frame='a'):
        
        w = terrain_map.w
        h = terrain_map.h
        _Map.__init__(self, w, h)
        
        self.ani_frame = ani_frame
        
    