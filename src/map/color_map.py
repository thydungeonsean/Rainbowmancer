from src.map._map import _Map


class ColorMap(_Map):

    def __init__(self, terrain_map, color):

        w = terrain_map.w
        h = terrain_map.h

        _Map.__init__(self, w, h)
        self.base = terrain_map
        self.color = color
        self.init_map()

        self.sources = {}
        self.inv_sources = {}

    def init_map(self):
        for point in self.all_points:
            self.set_tile(0, point)

    def add_source(self, point, strength):

        self.sources[point] = strength
        try:
            self.inv_sources[strength].append(point)
        except KeyError:
            self.inv_sources[strength] = [point]
        self.compute_map()

    def compute_map(self):        

        points = []

        for i in range(5, 0, -1):
            if i in self.inv_sources.keys():
                points.extend(self.inv_sources[i])
            for p in points:
                if i > self.get_tile(p):
                    self.set_tile(i, p)
            points = self.get_next_edge(points)
                        
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
    
