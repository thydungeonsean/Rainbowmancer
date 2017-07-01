from src.image.tileset import TileSet
from icon import Icon


class CrystalIcon(Icon):

    def __init__(self, coord, color):

        image = TileSet.get_icon_tiles().get_tile_image(''.join((color, '_crystal')))
        w = image.rect.w
        h = image.rect.h

        Icon.__init__(self, coord, w, h, image, color=color)

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
