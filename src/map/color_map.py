from src.map._map import _Map


class ColorMap(_Map):
    def __init__(self, master, terrain_map, colors):

        self.master = master
        self.fov_map = self.master.level.fov_map

        w = terrain_map.w
        h = terrain_map.h

        _Map.__init__(self, w, h)
        self.terrain_map = terrain_map
        self.colors = colors

        self.needs_recompute = False

    def clear_map(self):
        for point in self.all_points:
            self.set_tile(0, point)

    def change_map(self):
        self.needs_recompute = True

    def valid_color(self, source):
        return source.color in self.colors

    def compute_map(self):

        self.needs_recompute = False
        old = [x[:] for x in self.map]
        self.clear_map()  # otherwise it will be messy added and removing sources

        points = []

        for i in range(5, 0, -1):
            for source in filter(lambda s: self.valid_color(s), self.master.sources):
                if source.strength == i:
                    points.append(source.coord)
            for p in points:
                if i > self.get_tile(p):
                    self.set_tile(i, p)
            points = self.get_next_edge(points)

        diff = set()
        for x, y in self.all_points:
            if old[x][y] != self.get_tile(x, y):
                diff.add((x, y))

        return diff

    def get_next_edge(self, points):
        edge = set()
        for point in points:
            adj = set(self.get_adj(point))
            edge.update(adj)
        return list(edge)

    def print_map(self):

        for y in range(self.h):
            line = []
            for x in range(self.w):
                v = self.get_tile(x, y)
                if v == 0:
                    token = ' '
                else:
                    token = str(v)
                line.append(token)
            print ''.join(line)
