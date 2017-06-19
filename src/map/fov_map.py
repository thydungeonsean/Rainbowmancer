from src.libtcod import libtcodpy as libtcod


class FOVMap(object):

    SIGHT_RADIUS = 7
    LIGHT_WALLS = True
    ALGO = 4

    # turn of fov
    def all_visible(self, point):
        return self.explore_map.get(point) is not None

    def __init__(self, level, pre_explored=False, fov_on=True):

        self.level = level
        self.player = None

        self.w = None
        self.h = None

        self.map = None

        self.recompute = True

        self.visible = set()
        self.explore_map = {}

        self.pre_explored = pre_explored

        if not fov_on:
            self.pre_explored = True
            self.point_is_visible = self.all_visible

    # init fov
    def init_fov_map(self):

        self.w = self.level.terrain_map.w
        self.h = self.level.terrain_map.h
        self.map = libtcod.map_new(self.w, self.h)
        for point in self.level.terrain_map.all_points:
            self.set_fov_map_point(point)

        if self.pre_explored:
            self.pre_explore_map()
            self.level.redraw_manager.set_fov_redraw(self.explore_map.keys())

    def set_player(self, player):
        self.player = player

    def set_fov_map_point(self, (x, y)):
        libtcod.map_set_properties(self.map, x, y, self.point_transparent((x, y)), True)

    def point_transparent(self, point):

        wall = self.level.terrain_map.get_tile(point) in (1, 2)
        if wall:
            return False

        objects = self.level.game.objects
        blockers = filter(lambda x: x.block_sight and x.coord == point, objects)
        if blockers:
            return False

        return True

    # make single point fov changes on the fly (for open and close doors / abilities / spells)
    def update_point(self, point):
        self.set_fov_map_point(point)
        self.needs_recompute()

    # toggle recomputing, and recomputing
    def needs_recompute(self):
        self.recompute = True

    ###############################################
    # main computing function - center is coord of FOV source, if None, player is center
    def recompute_fov(self, center=None):

        cls = FOVMap
        self.recompute = False

        if center is None:
            x, y = self.player.coord
        else:
            x, y = center

        libtcod.map_compute_fov(self.map, x, y, cls.SIGHT_RADIUS, cls.LIGHT_WALLS, cls.ALGO)

        new_visible = self.get_visible_points((x, y))
        redraw = list(new_visible.symmetric_difference(self.visible))
        self.set_visible(new_visible)
        self.level.redraw_manager.set_fov_redraw(redraw)

    def get_visible_points(self, (px, py)):

        visible = set()

        for x in range(px-10, px+11):
            for y in range(py-10, py+11):
                if self.point_is_visible((x, y)):
                    visible.add((x, y))
                    self.explore((x, y))
        return visible

    def set_visible(self, new):
        self.visible = new

    ################################################
    # getting values from map
    def point_is_visible(self, (x, y)):
        return libtcod.map_is_in_fov(self.map, x, y)
    ################################################

    def explore(self, point):
        self.explore_map[point] = True

    def is_explored(self, point):
        return self.explore_map.get(point, False)

    def pre_explore_map(self):

        t_map = self.level.terrain_map
        floor = list(filter(lambda x: t_map.get_tile(x) not in (1, 2), t_map.all_points))

        touched = set()
        edge = []

        for point in floor:
            if point not in touched:
                edge.append(point)
                while edge:
                    for p in edge:
                        touched.add(p)
                    next_edge = self.get_next_edge(edge, t_map)
                    edge = list(filter(lambda x: t_map.get_tile(x) not in (1, 2) and x not in touched, next_edge))

    def get_next_edge(self, edge, t_map):
        next = set()
        for point in edge:
            adj = t_map.get_adj(point, diag=True)
            for a in adj:
                next.add(a)
                self.explore(a)
        return list(next)
