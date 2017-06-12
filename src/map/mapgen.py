from master_map import MasterMap
from terrain_map import TerrainMap
from random import *


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

    ROOM_MIN_W = 3
    ROOM_MAX_W = 9
    ROOM_MIN_H = 3
    ROOM_MAX_H = 7

    @classmethod
    def generate_terrain_map(cls, w, h, rooms=20, map_seed=None):
        if map_seed is None:
            map_seed = randint(0, 9999)
        seed(map_seed)

        t = TerrainMap(w, h, map_seed)

        cls.add_rooms(t, rooms)

    @classmethod
    def add_rooms(cls, t, rooms):

        room_count = 0
        attempts = 200
        while room_count < rooms:

            r = cls.get_room(t)
            if r:
                room_count += 1

            attempts -= 1
            if attempts <= 0:
                break

    @classmethod
    def get_room(cls, t):

        w = randint(cls.ROOM_MIN_W, cls.ROOM_MAX_W)
        h = randint(cls.ROOM_MIN_H, cls.ROOM_MAX_H)

        w_bound = t.w - w - 1
        h_bound = t.h - h - 1

        x = randint(1, w_bound)
        y = randint(1, h_bound)

        for ry in range(y, y + h + 1):
            for rx in range(x, x + w + 1):
                if t.get_tile(rx, ry) != 1:
                    return False

        for ry in range(y, y + h + 1):
            for rx in range(x, x + w + 1):
                t.set_tile(0, (rx, ry))
        return True

    ####################################################################################################################
    # cave map generator
    ####################################################################################################################

    DEATH_LIMIT = 4
    BIRTH_LIMIT = 3
    START_BIRTH = 45
    NUMBER_PASSES = 2

    @classmethod
    def generate_terrain_map_cave(cls, w, h, map_seed=None):
        if map_seed is None:
            map_seed = randint(0, 9999)
        seed(map_seed)

        cw = w - 2
        ch = h - 2

        cave_map = [[randint(1, 100) <= cls.START_BIRTH for my in range(ch)] for mx in range(cw)]

        for i in range(cls.NUMBER_PASSES):
            cave_map = cls.run_cellular_automata(cave_map, cw, ch)

        cave_map = cls.clean_cave_map(cave_map, cw, ch)

        t = TerrainMap(w, h, map_seed)
        for px, py in t.all_points:
            try:
                if cave_map[px][py]:
                    t.set_tile(0, (px+1, py+1))
            except IndexError:
                pass

        return t

    @classmethod
    def run_cellular_automata(cls, old_cave_map, w, h):

        new_map = [[False for my in range(h)] for mx in range(w)]

        for y in range(h):
            for x in range(w):

                neighbours = cls.count_neighbours(old_cave_map, (x, y), w, h)

                if old_cave_map[x][y]:
                    if neighbours < cls.DEATH_LIMIT:
                        new_map[x][y] = False
                    else:
                        new_map[x][y] = True
                else:
                    if neighbours > cls.BIRTH_LIMIT:
                        new_map[x][y] = True
                    else:
                        new_map[x][y] = False

        return new_map

    @classmethod
    def count_neighbours(cls, cave_map, (px, py), w, h):

        count = 0

        for y in range(py - 1, py + 2):
            for x in range(px - 1, px + 2):
                if x < 0 or y < 0 or x >= w or y >= h:
                    pass
                elif cave_map[x][y]:
                    count += 1

        return count

    @classmethod
    def clean_cave_map(cls, cave_map, w, h):

        # remove diagonal only connections

        return cave_map
