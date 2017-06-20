

class PathFindingMap(object):

    def __init__(self, level):

        self.level = level

        self.approach_map = None
        self.range_map = None

    @property
    def terrain(self):
        return self.level.terrain_map

    def compute(self):

        player = self.level.game.player.coord

        self.approach_map = self.get_dijkstra([player])
        self.range_map = self.get_dijkstra(self.get_range_source(player))

    def get_next_edge(self, edge):

        next_edge = set()

        for point in edge:
            adj = self.terrain.get_adj(point)
            for a in adj:
                next_edge.add(a)
        return list(next_edge)

    def get_dijkstra(self, edge):
        d_map = {}

        touched = set()
        value = 0

        while edge:
            for point in edge:
                touched.add(point)
                if d_map.get(point) is None:
                    d_map[point] = value
                elif value < d_map.get(point):
                    d_map[point] = value

            next_edge = self.get_next_edge(edge)
            edge = list(filter(lambda x: self.terrain.get_tile(x) in (0, 3) and x not in touched, next_edge))

            value += 1

        return d_map

    def get_range_source(self, (x, y)):

        target_locations = []

        for i in range(2, 8):
            target_locations.extend([(x+i, y), (x-i, y), (x, y+i), (x, y-i)])

        target_locations = list(filter(self.level.fov_map.point_is_visible, target_locations))

        return target_locations

