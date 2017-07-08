import pygame


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

        map_min_x, map_min_y, map_max_x, map_max_y = self.get_full_screen_bounds()
        if self.screen_mode == 'full':
            min_x = map_min_x
            min_y = map_min_y
            max_x = map_max_x
            max_y = map_max_y
        else:  # zoomed
            zoom_min_x, zoom_min_y, zoom_max_x, zoom_max_y = self.get_zoomed_screen_bounds()
            min_x = max((map_min_x, zoom_min_x))
            min_y = max((map_min_y, zoom_min_y))
            max_x = min((map_max_x, zoom_max_x))
            max_y = min((map_max_y, zoom_max_y))

        return min_x <= x < max_x and min_y <= y < max_y

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

        x, y = pygame.mouse.get_pos()

        if self.screen_mode == 'full':
            return self.get_full_mouse_coord((x, y))
        else:
            return self.get_zoomed_mouse_coord((x, y))

    def get_full_mouse_coord(self, (mx, my)):

        x = mx / 16
        y = my / 24

        if self.in_bounds((x, y)):
            return x, y
        else:
            return None

    def get_zoomed_mouse_coord(self, (mx, my)):
        sx, sy = self.get_screen_coord()
        x = (mx-56) / (16 * 2) + sx
        y = my / (24 * 2) + sy

        if self.in_bounds((x, y)):
            return x, y
        else:
            return None
