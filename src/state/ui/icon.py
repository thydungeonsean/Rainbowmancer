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
        self.coord = (x, y)
        self.image.position_pixel((x, y))

    def point_is_over(self, (x, y)):

        cx, cy = self.coord
        return cx <= x < cx + self.w and cy <= y < cy + self.h

    def click(self, (x, y)):
        if self.point_is_over((x, y)):
            print 'clicked icon ' + str(self)
            return True
        else:
            return False

    def right_click(self, (x, y)):
        if self.point_is_over((x, y)):
            print 'right clicked icon ' + str(self)
            return True
        else:
            return False

