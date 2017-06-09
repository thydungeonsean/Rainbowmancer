from _map import _Map


class TerrainMap(_Map):

    key = {
        0: 'floor',
        1: 'wall',
        2: 'door',
        3: 'brazier',
        4: 'stalagtite',
        5: 'large_crystal',
        6: 'small_crystal'
    }

    def __init__(self, w, h):
        
        _Map.__init__(self, w, h)
        
    def get_tile_id(self, point):
        return TerrainMap.key[self.get_tile(point)]

    def set_map(self, t_map):
        self.map = t_map
