

class Pointer(object):
    modes = {
        0: 'mouse',
        1: 'keys'
    }

    def __init__(self, game):

        self.game = game

        self.mode = 0

        self.coord = None

    def switch_mouse_mode(self):
        self.mode = 0
        self.clear_coord()

    def switch_keys_mode(self, start=None):
        self.mode = 1
        # set start coord here
        if self.coord is None:
            if start is None:
                self.set_coord(self.game.player.coord)
            else:
                self.set_coord(start)

    def mouse_moved(self):
        self.switch_mouse_mode()
        self.set_coord((self.game.game_display.get_mouse_coord()))

    def clear_coord(self):
        self.coord = None

    def set_coord(self, coord):
        self.coord = coord

    def move_up(self):
        if self.coord is not None:
            x, y = self.coord
            ny = y - 1
            if self.game.game_display.in_bounds((x, ny)):
                self.set_coord((x, ny))

    def move_down(self):
        if self.coord is not None:
            x, y = self.coord
            ny = y + 1
            if self.game.game_display.in_bounds((x, ny)):
                self.set_coord((x, ny))

    def move_left(self):
        if self.coord is not None:
            x, y = self.coord
            nx = x - 1
            if self.game.game_display.in_bounds((nx, y)):
                self.set_coord((nx, y))

    def move_right(self):
        if self.coord is not None:
            x, y = self.coord
            nx = x + 1
            if self.game.game_display.in_bounds((nx, y)):
                self.set_coord((nx, y))

    def update_mouse_coord(self):
        return self.game.game_display.get_mouse_coord()
