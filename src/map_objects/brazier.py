from map_object import MapObject
from components.light_component import LightComponent


class Brazier(MapObject):

    def __init__(self, map, coord):

        MapObject.__init__(self)

        self.set_map(map)
        self.set_coord(coord)

        self.state = 0

        self.check_if_ignited()

    def check_if_ignited(self):

        # TODO wanted braziers that start in color zones to be ignited with that color, but this isn't working
        # for some reason?  not big priority
        # color = self.map.color_map.get_tile_hue_name(self.coord)
        # print color
        pass

    def light(self, color):
        self.state = 1
        self.change_tile()
        self.light_component = LightComponent(self, self.map, color, 3)

    def douse(self):
        if self.state == 1:
            self.change_tile()
            self.light_component.kill()
            self.light_component = None
            self.state = 0

    def change_tile(self):

        tile_key = {0: 20, 1: 21}  # off and lit images

        self.map.tile_map.set_tile(tile_key[self.state], self.coord)
        if self.map.map_image is not None:
            self.map.map_image.add_to_redraw(self.coord)
            self.map.map_image.redraw_tiles()
