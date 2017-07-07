

class GameDisplay(object):

    zoom_screen_w = 9
    zoom_screen_h = 7

    def __init__(self, game):

        self.game = game

        self.screen_mode = 'zoomed'

    def switch_screen_mode(self):
        if self.screen_mode == 'full':
            self.screen_mode = 'zoomed'
            self.game.sub_screen.fill((0, 0, 0))
            self.game.draw_full()
        elif self.screen_mode == 'zoomed':
            self.screen_mode = 'full'

    def in_bounds(self, (x, y)):

        if self.screen_mode == 'full':
            min_x, min_y, max_x, max_y = self.get_full_screen_bounds()
        else:  # zoomed
            min_x, min_y, max_x, max_y = self.get_zoomed_screen_bounds()

        return min_x <= x < max_x and min_y <= y < max_x

    def get_full_screen_bounds(self):

        min_x = 0
        min_y = 0

        max_x = self.game.level.terrain_map.w
        max_y = self.game.level.terrain_map.h

        return min_x, min_y, max_x, max_y

    def get_zoomed_screen_bounds(self):

        min_x, min_y = self.get_screen_coord()
        max_x = min_x + (GameDisplay.zoom_screen_w * 2) + 1
        max_y = min_y + (GameDisplay.zoom_screen_h * 2) + 1

        return min_x, min_y, max_x, max_y

    def get_screen_coord(self):

        x, y = self.game.player.coord

        sx = x - GameDisplay.zoom_screen_w
        sy = y - GameDisplay.zoom_screen_h

        return sx, sy

    def get_screen_pix_coord(self):

        x, y = self.get_screen_coord()
        return x * -16, y * -24

    def get_mouse_coord(self):

        return None
