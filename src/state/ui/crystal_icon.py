from src.image.tileset import TileSet
from icon import Icon


class CrystalIcon(Icon):

    def __init__(self, panel, coord, color):

        image = TileSet.get_icon_tiles().get_tile_image(''.join((color, '_crystal')))
        w = image.rect.w
        h = image.rect.h
        self.color_name = color
        Icon.__init__(self, coord, w, h, image, color=color)

        self.panel = panel

        self.tick = 0
        self.count = 0

        self.state = 0

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
        else:
            color = self.color_component.ready_shade()
            self.image.recolor(color)

        self.image.draw(surface)

    def activate(self):
        self.glow = True
        self.state = 1

    def deactivate(self):
        self.glow = False
        self.count = 0
        self.tick = 0
        self.state = 0

    def click(self, (x, y)):
        if self.state == 0:
            return False
        if self.point_is_over((x, y)):
            self.panel.ui.game.active_ability.clicked_crystal(self.color_name)
            return True
        else:
            return False
