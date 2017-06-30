from panel import Panel
from src.image.tileset import TileSet
from src.color.color_palette import hue_codes, hue_key
import pygame


class CrystalPanel(Panel):

    w = 240
    h = 240

    x = 960 - w
    y = 720 - h
    coord = (x, y)

    icon_y = 240 - 80
    icon_x_offset = 19

    bar_y = icon_y

    bar_w = 23
    bar_margin = (32 - 24) / 2
    bar_chunk_h = 12

    level_w = 23 + 4

    def __init__(self, ui):
        pix_w = CrystalPanel.w
        pix_h = CrystalPanel.h
        coord = CrystalPanel.coord

        self.crystal_inventory = None
        Panel.__init__(self, ui, pix_w, pix_h, coord=coord)

        self.crystals = {}

        self.inventory = None

    def load_player(self):
        self.inventory = self.ui.game.player.crystal_inventory
        self.needs_update = True

        self.initialize()

    def initialize(self):

        cls = CrystalPanel
        colors = ('red', 'yellow', 'green', 'cyan', 'blue', 'purple')

        x = 0

        for color in colors:

            # create crystal icon
            crystal = CrystalIcon(color)
            self.crystals[color] = crystal
            crystal.position((self.x + self.get_icon_x(x), self.y + cls.icon_y))
            self.add_element(crystal)

            x += 1

        self.draw_bars()

    @staticmethod
    def get_icon_x(x):
        return CrystalPanel.icon_x_offset + (x * 34)

    def update(self):
        self.needs_update = False

        self.border.draw(self.surface)
        self.draw_bars()

    def draw_bars(self):

        cls = CrystalPanel
        colors = ('red', 'yellow', 'green', 'cyan', 'blue', 'purple')

        x = 0

        for color in colors:

            level = self.inventory.crystal_level[color]
            if level != 0:

                r = pygame.Rect((0, 0), (cls.level_w, cls.bar_chunk_h * level + 4))
                r.bottomleft = (self.get_icon_x(x) + cls.bar_margin - 2, cls.bar_y + 2)

                pygame.draw.rect(self.surface, (255, 255, 255), r, 1)

            num = self.inventory.crystal_num[color]
            if num < 1:
                x += 1
                continue

            c = hue_key[hue_codes[color]][4]

            bar = pygame.Surface((cls.bar_w, num * cls.bar_chunk_h)).convert()
            bar.fill(c)
            br = bar.get_rect()
            br.bottomleft = (self.get_icon_x(x) + cls.bar_margin, cls.bar_y)

            self.surface.blit(bar, br)

            x += 1







from src.map_objects.components.color_component import ColorComponent


class CrystalIcon(object):

    def __init__(self, color):
        self.image = TileSet.get_icon_tiles().get_tile_image(''.join((color, '_crystal')))
        self.color_component = ColorComponent(self, color=color)
        self.base_color = self.color_component.get_base_color()
        self.image.recolor(self.base_color)
        self.glow = True

        self.tick = 0
        self.count = 0

    def draw(self, surface, tick):

        if self.glow:

            color = self.color_component.get_boosted_color(self.base_color, self.tick)
            self.image.recolor(color)

            self.count += 1
            if self.count >= 5:
                self.count = 0
                self.tick += 1
                if self.tick > 59:
                    self.tick = 0

        self.image.draw(surface)

    def position(self, (x, y)):
        self.image.position_pixel((x, y))
