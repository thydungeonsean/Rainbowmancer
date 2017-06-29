from tileset import TileSet
import pygame


class PanelBorder(object):
    # this is purely an image

    min_w = 2
    min_h = 2

    tile_w = 16
    tile_h = 24

    def __init__(self, **kwargs):

        self.tileset = TileSet.get_border_tiles()

        self.w = PanelBorder.min_w
        self.h = PanelBorder.min_h

        self.pix_w = self.w * PanelBorder.tile_w
        self.pix_h = self.h * PanelBorder.tile_h

        if kwargs.get('pix_w') is not None:
            self.set_width(kwargs['pix_w'])
        elif kwargs.get('w') is not None:
            self.w = kwargs['w']
            self.pix_w = self.w * PanelBorder.tile_w

        if kwargs.get('pix_h') is not None:
            self.set_height(kwargs['pix_h'])
        elif kwargs.get('h') is not None:
            self.h = kwargs['h']
            self.pix_h = self.h * PanelBorder.tile_h

        self.image = self.set_image()
        self.rect = self.image.get_rect()

    def set_width(self, pix_w):
        pix_w = max((PanelBorder.min_w * PanelBorder.tile_w, pix_w))
        self.pix_w = pix_w
        self.w = pix_w / PanelBorder.tile_w

    def set_height(self, pix_h):
        pix_h = max((PanelBorder.min_h * PanelBorder.tile_h, pix_h))
        self.pix_h = pix_h
        self.h = pix_h / PanelBorder.tile_h

    def set_image(self):

        image = pygame.Surface((self.pix_w, self.pix_h)).convert()

        for y in range(self.h):
            for x in range(self.w):

                tile = self.get_top_left_tile((x, y))
                if tile is not None:
                    tile.position_pixel((x * PanelBorder.tile_w, y * PanelBorder.tile_h))
                    tile.draw(image)

        self.draw_bottom_right_border(image)

        return image

    def get_top_left_tile(self, (x, y)):

        if y == 0 and x == 0:
            return self.tileset.get_tile_image('top_left')
        elif x == 0:
            return self.tileset.get_tile_image('left')
        elif y == 0:
            return self.tileset.get_tile_image('top')

        return None

    def draw_bottom_right_border(self, image):

        for x in range(self.w):
            if x == 0:
                tile = self.tileset.get_tile_image('bottom_left')
            else:
                tile = self.tileset.get_tile_image('bottom')

            tile.position_pixel((x * PanelBorder.tile_w, self.pix_h - PanelBorder.tile_h))
            tile.draw(image)

        for y in range(self.h):
            if y == 0:
                tile = self.tileset.get_tile_image('top_right')
            else:
                tile = self.tileset.get_tile_image('right')

            tile.position_pixel((self.pix_w - PanelBorder.tile_w, y * PanelBorder.tile_h))
            tile.draw(image)

        bottom_right = self.tileset.get_tile_image('bottom_right')
        bottom_right.position_pixel((self.pix_w - PanelBorder.tile_w, self.pix_h - PanelBorder.tile_h))
        bottom_right.draw(image)

    def draw(self, surface):

        surface.blit(self.image, self.rect)

