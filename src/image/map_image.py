import pygame
from tileset import TileSet


class MapImage(object):
    TILEW = 16
    TILEH = 24

    def __init__(self, m_map):

        self.map = m_map

        self.tileset = TileSet.get_enviro_tiles()

        self.needs_redraw = True

        self.images = {
            ('a', 0): None,
            ('b', 0): None,
            ('a', 1): None,
            ('b', 1): None
        }

        self.rect = None

        self.init_map_images()

        self.redraw_tile_list = []  # give it a list of coords. will go through and redraw those coords

    def set_redraw(self):
        self.needs_redraw = True
        # redraw if:
        #     light sources changes
        #     player moves (fov changes)
        #     tile changes

    def init_map_images(self):

        mw = self.map.w * MapImage.TILEW
        mh = self.map.h * MapImage.TILEH

        self.images[('a', 0)] = pygame.Surface((mw, mh)).convert()
        self.images[('b', 0)] = pygame.Surface((mw, mh)).convert()
        self.images[('a', 1)] = pygame.Surface((mw, mh)).convert()
        self.images[('b', 1)] = pygame.Surface((mw, mh)).convert()

        self.rect = self.images[('a', 0)].get_rect()

        self.render_all_maps()

    def render_all_maps(self):

        self.render_map(('a', 0))
        self.render_b_map(0)

        self.render_map(('a', 1))
        self.render_b_map(1)

    def draw_tile_batch(self, surface, points, (ani, col_mod)):

        for point in points:
            self.draw_tile(surface, point, (ani, col_mod))

    def draw_tile(self, surface, (px, py), (ani, col_mod)):

        tl_map = self.map.tile_map
        cls = MapImage

        tile_key = tl_map.get_tile_key((px, py))
        if tl_map.point_is_animated((px, py)):
            tile_key = '_'.join((tile_key, ani))

        color = self.map.color_map.get_tile_color(col_mod, (px, py))

        tile = self.tileset.get_tile_image(tile_key)
        tile.recolor(color)
        tile.position((px, py))

        tile.draw(surface)

    def render_map(self, map_id):

        points = self.map.terrain_map.all_points
        self.draw_tile_batch(self.images[map_id], points, map_id)

    def render_b_map(self, col_mod):

        img = self.images[('b', col_mod)]
        img.blit(self.images[('a', col_mod)], img.get_rect())  # copy a_map onto surface

        # get ani tiles and only update those
        points = list(filter(self.map.tile_map.point_is_animated, self.map.tile_map.all_points))

        self.draw_tile_batch(img, points, ('b', col_mod))

    def draw(self, surface, tick):

        # or get map_id from other context
        map_id = self.get_map_id(tick)
        surface.blit(self.images[map_id], self.rect)

    def redraw_tile(self, point):

        cls = MapImage
        px, py = point

        tile_key = self.map.tile_map.get_tile_key(point)
        animated = False
        if self.map.tile_map.point_is_animated(point):
            a_key = '_'.join((tile_key, 'a'))
            b_key = '_'.join((tile_key, 'b'))
            animated = True

        col_0 = self.map.color_map.get_tile_color(0, point)
        col_1 = self.map.color_map.get_tile_color(1, point)

        if not animated:
            tile = self.tileset.get_tile_image(tile_key)
            tile.recolor(col_0)
            tile.position((px, py))
            tile.draw(self.images[('a', 0)])
            tile.draw(self.images[('b', 0)])
            tile.recolor(col_1)
            tile.draw(self.images[('a', 1)])
            tile.draw(self.images[('b', 1)])
        else:
            tile_a = self.tileset.get_tile_image(a_key)
            tile_a.recolor(col_0)
            tile_a.position((px, py))
            tile_a.draw(self.images[('a', 0)])
            tile_a.recolor(col_1)
            tile_a.draw(self.images[('a', 1)])

            tile_b = self.tileset.get_tile_image(b_key)
            tile_b.recolor(col_0)
            tile_b.position((px, py))
            tile_b.draw(self.images[('b', 0)])
            tile_b.recolor(col_1)
            tile_b.draw(self.images[('b', 1)])

    def redraw_tiles(self):

        for point in self.redraw_tile_list:
            self.redraw_tile(point)

        del self.redraw_tile_list[:]
        self.needs_redraw = False

    def add_to_redraw(self, point):

        self.set_redraw()
        self.redraw_tile_list.append(point)

    def add_batch_to_redraw(self, points):
        for point in points:
            self.add_to_redraw(point)

    @staticmethod
    def get_map_id(tick):
        if tick < 15:
            return 'a', 0
        elif tick < 30:
            return 'b', 0
        elif tick < 45:
            return 'a', 1
        else:
            return 'b', 1
