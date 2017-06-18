from src.map.color_map import ColorMap
from src.color.color_palette import get_shade, get_hue, hue_names


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

    def __init__(self, level):

        self.level = level
        terrain_map = self.level.terrain_map

        self.red_map = ColorMap(self, terrain_map, {'red', 'purple', 'yellow', 'white'})
        self.green_map = ColorMap(self, terrain_map, {'green', 'cyan', 'yellow', 'white'})
        self.blue_map = ColorMap(self, terrain_map, {'blue', 'purple', 'cyan', 'white'})

        self.sources = []

    def _get_tile_rgb(self, (x, y)):

        r = self.red_map.get_tile((x, y))
        g = self.green_map.get_tile((x, y))
        b = self.blue_map.get_tile((x, y))

        return r, g, b

    def get_tile_color(self, col_mod, (x, y)):

        r, g, b = self._get_tile_rgb((x, y))

        seen = self.level.fov_map.point_is_visible((x, y))

        return get_shade(r, g, b, col_mod, seen=seen)

    def get_reflected_color(self, (x, y)):

        r, g, b = self._get_tile_rgb((x, y))

        return get_shade(r, g, b, 1, reflected=True)

    def get_tile_hue(self, (x, y)):

        r, g, b = self._get_tile_rgb((x, y))

        return get_hue(r, g, b)

    def get_tile_hue_name(self, (x, y)):

        hue = self.get_tile_hue((x, y))

        return hue_names[hue]

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
        for map in needs_update:
            map.change_map()

    def recompute_maps(self):
        difference = set()
        for map in (self.red_map, self.green_map, self.blue_map):
            if map.needs_recompute:
                difference.update(map.compute_map())

        difference = filter(lambda x: self.level.fov_map.point_is_visible(x), list(difference))

        return difference

    def needs_recompute(self):

        for map in (self.red_map, self.green_map, self.blue_map):
            if map.needs_recompute:
                return True
        return False
