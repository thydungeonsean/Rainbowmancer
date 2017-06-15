from _map import _Map


class TerrainMap(_Map):

    key = {
        0: 'floor',
        1: 'wall',
        2: 'stone_wall',
        3: 'door',
        4: 'stalagtite',
        5: 'large_crystal',
        6: 'small_crystal',
        7: 'stairs',
        8: 'brazier'
    }

    def __init__(self, w, h, map_seed):
        
        _Map.__init__(self, w, h)
        self.map_seed = map_seed
        self.exit = None
        self.entrance = None

        self.secret = set()

    @staticmethod
    def start_value():
        return 1

    def set_exit(self, point):
        self.set_tile(7, point)
        self.exit = point

    def set_entrance(self, point):
        self.entrance = point

    def get_tile_id(self, point):
        return TerrainMap.key[self.get_tile(point)]

    def set_map(self, t_map):
        self.map = t_map
