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
    START_BIRTH = 40
    NUMBER_PASSES = 2

    ZONE_SIZE_THRESHOLD = 5
    SECRET_CAVE_CHANCE = 80
    SECRET_CAVE_THRESHOLD = 12

    STALAGTITE = .03
    BRAZIER = .01

    MAPFAILED = False

    @classmethod
    def mark_map_failed(cls):
        cls.MAPFAILED = True

    @classmethod
    def reset(cls):
        cls.MAPFAILED = False

    @classmethod
    def generate_terrain_map_cave(cls, w, h, map_seed=None):
        if map_seed is None:
            map_seed = randint(0, 9999)
        seed(map_seed)

        print map_seed

        cw = w - 2
        ch = h - 2

        generating = True
        c = 0

        while generating:

            cls.reset()

            cave_map = [[randint(1, 100) <= cls.START_BIRTH for my in range(ch)] for mx in range(cw)]

            for i in range(cls.NUMBER_PASSES):
                cave_map = cls.run_cellular_automata(cave_map, cw, ch)

            cave_map = cls.clean_cave_map(cave_map, cw, ch)

            terrain_map = cls.create_terrain_map(cave_map, w, h, map_seed)

            cls.get_cave_zones(terrain_map)

            cls.clear_stranded_doors(terrain_map)

            exit_placed = cls.set_exit(terrain_map)
            if not exit_placed:
                continue  # trash this map

            cls.set_entrance(terrain_map)
            cls.set_crystals(terrain_map, 10)

            cls.set_braziers(terrain_map)
            cls.set_stalagtites(terrain_map)

            if cls.check_map_connected(terrain_map):
                print 'map success'
            else:
                cls.mark_map_failed()

            if not cls.MAPFAILED:
                generating = False
            print c
            c += 1

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

        for y in range(0, h, 2):
            for x in range(0, w, 2):
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

        if square_value[0] == square_value[1] or square_value[2] == square_value[3]:  # doesn't need cleaning
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
            if t_map.get_tile(a) not in (1, 2):
                return True
        return False

    @classmethod
    def wall_is_horizontal(cls, t_map, (x, y)):
        below = x, y+1
        return t_map.point_in_bounds(below) and t_map.get_tile(below) not in (1, 2, 3)

    @classmethod
    def flood_zones(cls, t_map):

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
                    edge = list(filter(lambda x: t_map.get_tile(x) in (0, 3) and x not in touched, next_edge))
                zone_id += 1

        return point_zones, zone_lists

    @classmethod
    def get_cave_zones(cls, t_map):

        point_zones, zone_lists = cls.flood_zones(t_map)

        cls.clean_zones(t_map, point_zones, zone_lists)

        if len(zone_lists.keys()) > 1:
            cls.connect_zones(t_map, point_zones, zone_lists)

        # print zones
        # for y in range(t_map.h):
        #     line = []
        #     for x in range(t_map.w):
        #         a = point_zones.get((x, y))
        #         if a is not None:
        #             line.append(str(a))
        #         else:
        #             line.append(' ')
        #     print ''.join(line)

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
    def connect_zones(cls, t_map, point_zones, zone_lists):

        zone_order = sorted(zone_lists.keys(), key=lambda z: len(zone_lists[z]))
        largest = zone_order.pop()  # remove largest zone, don't need to connect it.

        secret_zones = []

        for zone_id in zone_order:

            zone_connectors = cls.get_zone_connectors(t_map, point_zones, zone_id)
            if len(zone_connectors) == 0:
                cls.dig_tunnel(t_map, point_zones, zone_lists, zone_id, largest)
            else:  # we either carve out a random connector to join zones or we leave it as a secret zone
                if len(zone_lists[zone_id]) < MapGen.SECRET_CAVE_THRESHOLD \
                        and randint(1, 100) <= MapGen.SECRET_CAVE_CHANCE:
                    secret_zones.append(zone_id)
                else:

                    opening = choice(zone_connectors)
                    if cls.valid_for_door(t_map, opening):
                        tile = 3
                    else:
                        tile = 0
                    t_map.set_tile(tile, opening)

        for z in secret_zones:
            for point in zone_lists[z]:
                t_map.secret.add(point)

        for point in zone_lists[largest]:
            t_map.main_zone.add(point)

        # remove anything unconnected
        # new_point_zones, new_zone_lists = cls.flood_zones(t_map)
        # largest = sorted(new_zone_lists.keys(), key=lambda z: len(new_zone_lists[z])).pop()
        # for point in cls.get_floor_set(t_map):
        #     if new_point_zones.get(point) != largest:  # not connected
        #         if point_zones.get(point) not in secret_zones:  # not secret
        #             t_map.set_tile(1, point)

    @classmethod
    def valid_for_door(cls, t_map, (x, y)):
        adj = ((x-1, y), (x+1, y), (x, y-1), (x, y+1))
        zone = [t_map.get_tile(a) for a in adj]
        return zone[0] == zone[1] and zone[2] == zone[3] and zone[0] != zone[2]

    @classmethod
    def get_zone_connectors(cls, t_map, point_zones, zone_id):

        return filter(lambda z: cls.wall_is_zone_connector(z, t_map, point_zones, zone_id),
                      cls.get_wall_edge_set(t_map))

    @classmethod
    def wall_is_zone_connector(cls, point, t_map, point_zones, zone_id):

        adj = t_map.get_adj(point)
        next_to_current_zone = False
        adj_zones = set()
        for a in adj:
            if point_zones.get(a) == zone_id:
                next_to_current_zone = True
            if point_zones.get(a) is not None:
                adj_zones.add(point_zones[a])
        return next_to_current_zone and len(adj_zones) > 1

    @classmethod
    def get_path(cls, t_map, edge, path_restriction, end_state):

        d_map = {}
        touched = set()
        value = 0

        end_point = None
        end = False

        while edge:
            for point in edge:
                touched.add(point)

                if d_map.get(point) is None:
                    d_map[point] = value
                elif value < d_map.get(point):
                    d_map[point] = value

                if end_state(point):
                    end_point = point
                    end = True
            if end:
                break
            next_edge = cls.get_next_edge(edge, t_map)
            next_edge = filter(lambda x: x not in touched, next_edge)
            edge = list(filter(path_restriction, next_edge))

            value += 1

        return d_map, end_point

    @classmethod
    def trace_path(cls, t_map, d_map, end):
        path = [end]
        point = end
        while d_map.get(point) != 0:

            adj = filter(lambda a: d_map.get(a) is not None, t_map.get_adj(point))
            shuffle(adj)

            adj = sorted(adj, key=lambda a: d_map.get(a))
            point = adj[0]
            path.append(point)

        return path

    @classmethod
    def dig_tunnel(cls, t_map, zones, zone_lists, zone_id, max):

        start = choice(zone_lists[zone_id])

        d_map, tunnel_end = cls.get_path(t_map, [start], lambda e: True,
                                         lambda e: zones.get(e) is not None and zones[e] == max)

        if tunnel_end is None:
            raise Exception('digging tunnel failed -- this should be impossible')

        tunnel = cls.trace_path(t_map, d_map, tunnel_end)

        for point in tunnel:
            t_map.set_tile(0, point)

        shuffle(tunnel)
        for point in tunnel:
            if cls.valid_for_door(t_map, point):
                t_map.set_tile(3, point)
                break

    @classmethod
    def set_exit(cls, t_map):

        valid_exits = filter(lambda e: cls.valid_exit(t_map, e), cls.get_hor_wall_set(t_map))

        if not valid_exits:
            placed = cls.force_exit(t_map)
        else:
            exit = choice(valid_exits)
            t_map.set_exit(exit)
            placed = True

        return placed

    @classmethod
    def force_exit(cls, t_map):

        force_exit_list = list(filter(lambda x: cls.valid_for_force_exit(t_map, x), t_map.main_zone))

        if not force_exit_list:
            return False

        exit = choice(force_exit_list)
        t_map.set_exit(exit)

        ex, ey = exit
        walls = ((ex-1, ey-1), (ex, ey-1), (ex+1, ey-1), (ex-1, ey), (ex+1, ey))

        for point in walls:
            t_map.set_tile(2, point)
        return True

    @classmethod
    def valid_for_force_exit(cls, t_map, (x, y)):

        force_zone = set()

        for zx in range(x-2, x+4):
            for zy in range(y-2, y+4):
                force_zone.add((zx, zy))

        for point in force_zone:
            if not t_map.point_in_bounds(point) or t_map.get_tile(point) != 0:
                return False

        return True

    @classmethod
    def valid_exit(cls, t_map, (x, y)):

        left = x-1, y
        right = x+1, y
        up = x, y - 1
        down = x, y + 1
        # TODO can't be in secret room??? or if in secret room, add another exit in main dungeon?
        return t_map.get_tile(left) == 1 and t_map.get_tile(right) == 1 and cls.wall_is_horizontal(t_map, left) and \
            cls.wall_is_horizontal(t_map, right) and t_map.get_tile(up) == 1 and down in t_map.main_zone

    @classmethod
    def set_entrance(cls, t_map):

        ex = t_map.exit

        d_map = cls.get_dijkstra(t_map, [ex])

        max_dist = max(d_map.values())
        if max_dist > 6:
            entrance_dist = max_dist - randint(3, 5)
        else:
            entrance_dist = max_dist

        valid_entrances = filter(lambda (k, v): v == entrance_dist, d_map.iteritems())
        assert valid_entrances
        entrance = choice(valid_entrances)[0]
        t_map.set_entrance(entrance)

    @classmethod
    def clear_stranded_doors(cls, t_map):

        doors = filter(lambda d: t_map.get_tile(d) == 3, t_map.all_points)
        for door in doors:
            if not cls.valid_for_door(t_map, door):
                t_map.set_tile(0, door)

    @classmethod
    def set_crystals(cls, t_map, num):

        d_map = cls.get_edge_dist_dijkstra(t_map)
        entrance_d_map = cls.get_entrance_dijkstra(t_map)

        crystal_map = []

        for i in range(num):
            cls.set_crystal(t_map, d_map, entrance_d_map, crystal_map)

    @classmethod
    def set_crystal(cls, t_map, d_map, entrance_d_map, crystal_map):

        optimal_distance = randint(2, 4)

        floor = cls.get_floor_set(t_map)

        weight_map = {}

        for point in floor:
            weight_map[point] = -1 * abs(optimal_distance - d_map[point]) + 5

            if entrance_d_map.get(point) is not None and entrance_d_map[point] < 10:
                weight_map[point] -= 10

            if point in t_map.secret:
                weight_map[point] += 5

            # adj_walls = cls.count_adj_walls(t_map, point)  # weights in favour of points adj to walls
            # if adj_walls == 2:
            #     weight_map[point] += 1
            # elif adj_walls == 3:
            #     weight_map[point] += 2

            x, y = point
            for cx, cy in crystal_map:
                if abs(x - cx) + abs(y - cy) < 10:
                    weight_map[point] -= 5

        crystal = sorted(weight_map.keys(), key = lambda x: weight_map[x]).pop()
        t_map.set_tile(5, crystal)
        crystal_map.append(crystal)

    @classmethod
    def count_adj_walls(cls, t_map, point):

        count = 0
        adj = t_map.get_adj(point)
        for a in adj:
            if t_map.get_tile(a) == 1:
                count += 1
        return count

    @classmethod
    def get_edge_dist_dijkstra(cls, t_map):

        return cls.get_dijkstra(t_map, list(cls.get_wall_edge_set(t_map)))

    @classmethod
    def get_entrance_dijkstra(cls, t_map):

        return cls.get_dijkstra(t_map, [t_map.entrance])

    @classmethod
    def get_dijkstra(cls, t_map, edge):
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

            next_edge = cls.get_next_edge(edge, t_map)
            edge = list(filter(lambda x: t_map.get_tile(x) in (0, 3) and x not in touched, next_edge))

            value += 1

        return d_map

    @classmethod
    def set_stalagtites(cls, t_map):

        floor = cls.get_floor_set(t_map)
        shuffle(floor)

        number = int(len(floor) * MapGen.STALAGTITE)
        placed = 0

        for point in floor:

            if cls.point_not_obstructing(t_map, point):
                t_map.set_tile(4, point)
                placed += 1

            if placed >= number:
                break

    @classmethod
    def point_not_obstructing(cls, t_map, point, safe=set()):

        adj = t_map.get_adj(point, diag=True)
        for a in adj:
            if t_map.get_tile(a) != 0 or a in safe:
                return False
        return True

    @classmethod
    def set_braziers(cls, t_map):

        floor = cls.get_floor_set(t_map)
        shuffle(floor)

        number = int(len(floor) * MapGen.BRAZIER)
        placed = 0

        for point in floor:

            if cls.point_not_obstructing(t_map, point):
                t_map.set_tile(8, point)
                placed += 1

            if placed >= number:
                break

    @classmethod
    def check_map_connected(cls, t_map):

        d_map, exit = cls.get_path(t_map, [t_map.entrance], lambda e: t_map.get_tile(e) in (0, 3, 5, 6, 7),
                                   lambda x: x == t_map.exit)

        # line = cls.trace_path(t_map, d_map, exit)
        # line.pop(0)
        # for point in line:
        #     t_map.set_tile(4, point)

        return exit is not None

