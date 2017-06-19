

class PathFindingMap(object):

    def __init__(self, level):

        self.level = level

    @property
    def terrain(self):
        return self.level.terrain_map

    def compute(self):
        pass

    def get_next_edge(self, edge):

        next = set()

        for point in edge:
            adj = self.terrain.get_adj(point)
            for a in adj:
                next.add(a)
        return list(next)

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