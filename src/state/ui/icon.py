from src.map_objects.components.color_component import ColorComponent


class Icon(object):

    def __init__(self, coord, w, h, image, color=None):

        self.image = image
        self.coord = coord
        self.w = w
        self.h = h

        self.color_component = ColorComponent(self, color=color)
        self.base_color = self.color_component.get_base_color()

        if self.image is not None:
            self.image.recolor(self.base_color)
            self.position(coord)

        self.glow = True

    def draw(self, surface, tick):
        self.image.draw(surface)

    def position(self, (x, y)):
        self.image.position_pixel((x, y))
