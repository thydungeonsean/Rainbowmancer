from image_component import ImageComponent
from color_component import ColorComponent


class MapObject(object):

    def __init__(self):

        self.map = None
        self.coord = None

        self.image_component = None
        self.color_component = None

        self.light_component = None

    def set_map(self, map):
        self.map = map

    def set_coord(self, coord):
        self.coord = coord

    def set_image(self, name):
        self.image_component = ImageComponent(self, name)

    def set_color(self, color):
        self.color_component = ColorComponent(self, color)

    def set_light(self, light):
        self.light_component = light

    def move(self, new):
        self.coord = new
        if self.light_component is not None:
            self.light_component.move(new)

    def draw(self, surface, tick):

        if self.image_component is not None:

            self.image_component.draw(surface, tick)
