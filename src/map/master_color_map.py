from src.map.color_map import ColorMap
from src.color.color_palette import get_shade


class MasterColorMap(object):

    key = {
        0: 'red',
        1: 'green',
        2: 'blue',
        3: 'yellow',
        4: 'purple',
        5: 'cyan',
        6: 'white'
    }

    encode = {v: k for (k, v) in key.iteritems()}

    def __init__(self, terrain_map):
        
        self.red_map = ColorMap(terrain_map, 'red')
        self.green_map = ColorMap(terrain_map, 'green')
        self.blue_map = ColorMap(terrain_map, 'blue')
        
    def get_tile_color(self, col_mod, *xargs):
            
        r = self.red_map.get_tile(*xargs)
        g = self.green_map.get_tile(*xargs)
        b = self.blue_map.get_tile(*xargs)
        
        return get_shade(r, g, b, col_mod)

    def add_source(self, color, point, strength):

        cls = MasterColorMap

        if color == 0 or cls.encode.get(color) == cls.encode['red']:
            self.add_red_source(point, strength)
        elif color == 1 or cls.encode.get(color) == cls.encode['green']:
            self.add_green_source(point, strength)
        elif color == 2 or cls.encode.get(color) == cls.encode['blue']:
            self.add_blue_source(point, strength)
        elif color == 3 or cls.encode.get(color) == cls.encode['yellow']:
            self.add_red_source(point, strength)
            self.add_green_source(point, strength)
        elif color == 4 or cls.encode.get(color) == cls.encode['purple']:
            self.add_red_source(point, strength)
            self.add_blue_source(point, strength)
        elif color == 5 or cls.encode.get(color) == cls.encode['cyan']:
            self.add_green_source(point, strength)
            self.add_blue_source(point, strength)
        elif color == 6 or cls.encode.get(color) == cls.encode['white']:
            self.add_red_source(point, strength)
            self.add_green_source(point, strength)
            self.add_blue_source(point, strength)

    def add_red_source(self, point, strength):
        self.red_map.add_source(point, strength)

    def add_green_source(self, point, strength):
        self.green_map.add_source(point, strength)

    def add_blue_source(self, point, strength):
        self.blue_map.add_source(point, strength)