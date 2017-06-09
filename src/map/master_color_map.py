from src.map.color_map import ColorMap
from src.color.color_palette import get_shade


class MasterColorMap(object):

    def __init__(self, terrain_map):
        
        self.red_map = ColorMap(terrain_map, 'red')
        self.green_map = ColorMap(terrain_map, 'green')
        self.blue_map = ColorMap(terrain_map, 'blue')
        
    def get_tile_color(self, col_mod, *xargs):
            
        # if not in FOV, return grey shade - no col_mod
            
        r = self.red_map.get_tile(*xargs)
        g = self.green_map.get_tile(*xargs)
        b = self.blue_map.get_tile(*xargs)
        
        return get_shade(r, g, b, col_mod)
