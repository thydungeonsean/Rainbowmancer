from src.map._map import _Map
from src.map.color_map import ColorMap
from src.color.color_palette import get_shade


class MasterColorMap(_Map):

    def __init__(self, terrain_map):
    
        w = terrain_map.w
        h = terrain_map.h
        
        _Map.__init__(self, w, h)
        
        self.red_map = ColorMap(terrain_map, 'red')
        self.green_map = ColorMap(terrain_map, 'green')
        self.blue_map = ColorMap(terrain_map, 'blue')
        
    def get_tile_color(self, *args)
            
        r = self.red_map.get_tile(*args)
        g = self.green_map.get_tile(*args)
        b = self.blue_map.get_tile(*args)
        
        return get_shade(r, g, b)
