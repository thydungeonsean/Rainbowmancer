from src.map.color_map import ColorMap
from src.color.color_palette import get_shade, get_hue


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

        self.red_map = ColorMap(self, terrain_map, {'red', 'purple', 'yellow', 'white'})
        self.green_map = ColorMap(self, terrain_map, {'green', 'cyan', 'yellow', 'white'})
        self.blue_map = ColorMap(self, terrain_map, {'blue', 'purple', 'cyan', 'white'})

        self.sources = []

    def get_tile_color(self, col_mod, *xargs):

        r = self.red_map.get_tile(*xargs)
        g = self.green_map.get_tile(*xargs)
        b = self.blue_map.get_tile(*xargs)

        return get_shade(r, g, b, col_mod)

    def get_reflected_color(self, *xargs):

        r = self.red_map.get_tile(*xargs)
        g = self.green_map.get_tile(*xargs)
        b = self.blue_map.get_tile(*xargs)

        return get_shade(r, g, b, 1, reflected=True)

    def get_tile_hue(self, *xargs):

        r = self.red_map.get_tile(*xargs)
        g = self.green_map.get_tile(*xargs)
        b = self.blue_map.get_tile(*xargs)

        return get_hue(r, g, b)

    def add_source(self, source):

        self.sources.append(source)
        self.update_maps(source)

    def remove_source(self, source):
        try:
            self.sources.remove(source)
            self.update_maps(source)
        except ValueError:
            print 'cannot remove %s from source list, it is not present' % (str(source.coord))

    def move_source(self, source):
        self.update_maps(source)

    def update_maps(self, source):

        needs_update = filter(lambda m: source.color in m.colors, (self.red_map, self.green_map, self.blue_map))
        # map(change_map, need_update)  # double check how that works
        for m in needs_update:
            m.change_map()

    def recompute_maps(self):
        difference = set()
        for map in (self.red_map, self.green_map, self.blue_map):
            if map.needs_recompute:
                difference.update(map.compute_map())

        return list(difference)

    def needs_recompute(self):

        for map in (self.red_map, self.green_map, self.blue_map):
            if map.needs_recompute:
                return True
        return False
