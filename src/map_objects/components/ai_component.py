from random import shuffle, choice


class AIComponent(object):

    states = {
        0: 'guard',
        1: 'wander',
        2: 'approach',
        3: 'stunned'
    }

    def __init__(self, owner):

        self.owner = owner
        self.state = choice((0, 1))

    def stun(self):
        self.state = 3

    def refresh(self):
        self.state = 0

    def run(self):
        self.check_state()
        self.run_state()

    def check_state(self):

        coord = self.owner.coord
        if self.state in (0, 1):  # check if sees the player
            if self.owner.map.fov_map.point_is_visible(coord):
                self.state = 2
        elif self.state == 2:  # if lost sight of player...
            if not self.owner.map.fov_map.point_is_visible(coord):
                self.state = 1

    def run_state(self):
        if self.state in (0, 3):
            # take turn on tracker
            # do nothing
            pass
        elif self.state == 1:
            self.wander()
        elif self.state == 2:
            self.engage()

    def wander(self):
        adj = self.get_adj(center=True)
        for point in adj:
            if self.owner.move_component.can_move(point):
                self.owner.move(point)
                self.owner.turn_component.take_turn()

    def get_adj(self, center=False):
        adj = self.owner.map.terrain_map.get_adj(self.owner.coord)
        if center:
            adj.append(self.owner.coord)
        shuffle(adj)
        return adj

    def engage(self):

        # if creature can trigger ability, it does it now and spends turn

        dijkstra = self.get_dijkstra()
        adj = self.get_adj()
        weight_map = {}
        for point in adj:
            value = dijkstra.get(point)
            if value is not None:
                weight_map[point] = value

        adj = sorted(weight_map.keys(), key=lambda x: weight_map[x])

        for point in adj:
            if self.owner.move_component.can_move(point):
                self.owner.move(point)
                self.owner.turn_component.take_turn()
                break



    def get_dijkstra(self):
        return self.owner.map.path_finding_map.approach_map
