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

    ZONE_SIZE_THRESHOLD = 5

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

        terrain_map = cls.create_terrain_map(cave_map, w, h, map_seed)

        z = cls.get_cave_zones(terrain_map)

        cls.set_exit(terrain_map)
        cls.set_entrance(terrain_map)

        return terrain_map

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

        for y in range(h-1):
            for x in range(w-1):
                cls.clean_square(cave_map, x, y)

        return cave_map

    @classmethod
    def clean_square(cls, cave_map, x, y):
        square_value = []
        square_coord = {}
        i = 0
        for sx in range(x, x+2):
            for sy in range(y, y+2):
                square_value.append(cave_map[x][y])
                square_coord[i] = (sx, sy)
                i += 1

        if square_value[0] == square_value[2] or square_value[1] == square_value[3]:  # doesn't need cleaning
            return

        if not square_value[0]:
            clear_x, clear_y = square_coord[choice((0, 3))]
        else:
            clear_x, clear_y = square_value[choice((1, 2))]

        cave_map[clear_x][clear_y] = True

    @classmethod
    def create_terrain_map(cls, cave_map, w, h, map_seed):

        t = TerrainMap(w, h, map_seed)
        for px, py in t.all_points:
            try:
                if cave_map[px][py]:
                    t.set_tile(0, (px + 1, py + 1))
            except IndexError:
                pass
        return t

    @classmethod
    def get_floor_set(cls, t_map):
        return filter(lambda x: t_map.get_tile(x) == 0, t_map.all_points)

    @classmethod
    def get_wall_set(cls, t_map):
        return filter(lambda x: t_map.get_tile(x) == 1, t_map.all_points)

    @classmethod
    def get_wall_edge_set(cls, t_map):
        walls = cls.get_wall_set(t_map)
        return filter(lambda w: cls.wall_is_edge(t_map, w), walls)

    @classmethod
    def get_hor_wall_set(cls, t_map):
        return filter(lambda w: cls.wall_is_horizontal(t_map, w), cls.get_wall_edge_set(t_map))

    @classmethod
    def wall_is_edge(cls, t_map, point):
        adj = t_map.get_adj(point)
        for a in adj:
            if t_map.get_tile(a) != 1:
                return True
        return False

    @classmethod
    def wall_is_horizontal(cls, t_map, (x, y)):
        below = x, y+1
        return t_map.point_in_bounds(below) and t_map.get_tile(below) != 1

    @classmethod
    def get_cave_zones(cls, t_map):

        floor = list(cls.get_floor_set(t_map))

        touched = set()
        edge = []
        point_zones = {}
        zone_lists = {}

        zone_id = 0

        for point in floor:
            if point not in touched:
                edge.append(point)
                while edge:
                    for p in edge:
                        touched.add(p)
                        point_zones[p] = zone_id
                        try:
                            zone_lists[zone_id].append(p)
                        except KeyError:
                            zone_lists[zone_id] = [p]
                    next_edge = cls.get_next_edge(edge, t_map)
                    edge = list(filter(lambda x: t_map.get_tile(x) == 0 and x not in touched, next_edge))
                zone_id += 1

        cls.clean_zones(t_map, point_zones, zone_lists)

        # for y in range(t_map.h):
        #     line = []
        #     for x in range(t_map.w):
        #         a = point_zones.get((x, y))
        #         if a is not None:
        #             line.append(str(a))
        #         else:
        #             line.append(' ')
        #     print ''.join(line)

        cls.clean_zones(t_map, point_zones, zone_lists)
        # connect zones

        return point_zones, zone_lists

    @classmethod
    def get_next_edge(cls, edge, t_map):
        next = set()
        for point in edge:
            adj = t_map.get_adj(point)
            for a in adj:
                next.add(a)
        return list(next)

    @classmethod
    def clean_zones(cls, t_map, point_zones, zone_lists):

        zone_sizes = [(k, len(v)) for (k, v) in zone_lists.iteritems()]

        too_small = []

        for z, size in zone_sizes:
            if size < MapGen.ZONE_SIZE_THRESHOLD:
                too_small.append(z)

        for zone in too_small:
            for point in zone_lists[zone]:
                t_map.set_tile(1, point)
                del point_zones[point]
            del zone_lists[zone]

    @classmethod
    def set_exit(cls, t_map):

        valid_exits = filter(lambda e: cls.valid_exit(t_map, e), cls.get_hor_wall_set(t_map))

        if not valid_exits:
            raise Exception('no valid exit on this map, need to create one')
            # create exit space
        else:
            exit = choice(valid_exits)
            t_map.set_exit(exit)

    @classmethod
    def valid_exit(cls, t_map, (x, y)):

        left = x-1, y
        right = x+1, y

        return t_map.get_tile(left) == 1 and t_map.get_tile(right) == 1 and cls.wall_is_horizontal(t_map, left) and \
            cls.wall_is_horizontal(t_map, right)

    @classmethod
    def set_entrance(cls, t_map):

        ex = t_map.exit

        d_map = {}

        edge = [ex]
        touched = set()
        value = 0

        while edge:
            for point in edge:
                touched.add(point)
                if d_map.get(point) is None:
                    d_map[point] = value
                elif value < d_map.get(point):
                    d_map[point] = value

            next_edge = cls.get_next_edge(edge, t_map)
            edge = list(filter(lambda x: t_map.get_tile(x) == 0 and x not in touched, next_edge))

            value += 1

        entrance_dist = max(d_map.values()) - randint(3, 5)
        valid_entrances = filter(lambda (k, v): v == entrance_dist, d_map.iteritems())
        entrance = choice(valid_entrances)[0]
        t_map.set_entrance(entrance)
