from master_map import MasterMap
from terrain_map import TerrainMap


class MapGen(object):

    def gen_demo(self):

        map = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 3, 1],
            [1, 0, 1, 2, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 1, 5, 0, 1, 0, 0, 4, 1, 1],
            [1, 1, 0, 0, 1, 1, 0, 4, 1, 1],
            [1, 1, 1, 0, 6, 1, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 3, 0, 0, 1],
            [1, 1, 0, 2, 0, 3, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

        m = MasterMap()
        t = TerrainMap(10, 10)
        t.set_map(map)

        m.set_terrain_map(t)
        m.initialize()
