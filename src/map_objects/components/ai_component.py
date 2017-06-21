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

        if self.state in (0, 1):  # check if sees the player
            if self.can_see_player():
                self.state = 2
        elif self.state == 2:  # if lost sight of player...
            if not self.can_see_player():
                self.state = 1

    def run_state(self):
        if self.state in (0, 3):  # stunned or waiting
            # do nothing
            self.owner.turn_component.take_turn()
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
        # also check for bump to attack?

        dijkstra = self.get_dijkstra()
        adj = self.get_adj()
        weight_map = {}
        for point in adj:
            value = dijkstra.get(point)
            if value is not None:
                weight_map[point] = value

        adj = sorted(weight_map.keys(), key=lambda x: weight_map[x])

        for point in adj:
            can_move = self.owner.move_component.can_move(point)
            can_bump, target = self.owner.move_component.can_bump(point)

            if can_move:
                self.owner.move(point)
                self.owner.turn_component.take_turn()
                break
            elif can_bump:
                self.owner.bump(target)
                self.owner.turn_component.take_turn()
                break

        # handle no moves, no bumps
        try_again = False
        for point in adj:
            monster = self.monster_on_point(point)
            if monster is not None and monster.turn_component.state in (0, 2):
                self.owner.turn_component.delay()
                try_again = True
                break
        # might need to enforce a retry limit counter per creature
        if not try_again:
            self.owner.turn_component.take_turn()  # completely blocked for the turn, pass

    def get_dijkstra(self):
        return self.owner.map.path_finding_map.approach_map

    def can_see_player(self):
        return self.owner.map.fov_map.point_is_visible(self.owner.coord)

    def monster_on_point(self, point):
        monster = None
        monsters = filter(lambda x: x.coord == point and x.object_type == 'monster', self.owner.map.game.objects)
        if monsters:
            monster = monsters.pop()

        return monster

