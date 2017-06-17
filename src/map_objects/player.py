from actor import Actor


class Player(Actor):

    move_code = {
        'up': (0, -1),
        'down': (0, 1),
        'right': (1, 0),
        'left': (-1, 0)
    }

    def __init__(self, coord, player_key):

        Actor.__init__(self, None, coord, player_key, color=None)

    def initialize(self, level):
        self.set_map(level)
        self.move_component.map = level

    def move_player(self, code):

        mx, my = Player.move_code[code]
        new = self.coord[0]+mx, self.coord[1]+my
        if self.move_component.can_move(new):
            self.move(new)
            self.map.fov_map.recompute_fov()
