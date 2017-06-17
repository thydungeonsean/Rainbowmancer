from map_object import MapObject
from components.light_component import LightComponent


class Crystal(MapObject):

    def __init__(self, map, coord, color):

        MapObject.__init__(self)
        self.set_map(map)
        self.set_coord(coord)
        self.set_color(color)
        self.set_light(self.get_light_component(color))
        self.set_image('large_crystal')

    def get_light_component(self, color):

        return LightComponent(self, self.map, color, 5)
