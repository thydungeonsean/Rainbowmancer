from _map import _Map
from tile_map import TileMap
from master_color_map import MasterColorMap


class TerrainMap(_Map):

    key = {
    0: 'floor',
    1: 'wall',
    2: 'door',
    3: 'crystal',
    4: 'brazier',
    5: 'stalagtite'
    }

    def __init__(self, w, h):
        
        _Map.__init__(self, w, h)
        
        self.tile_map = TileMap(self)
        self.color_map = MasterColorMap(self)
        
        self.init()
        
    def init(self):
        self.tile_map.init()
    
        