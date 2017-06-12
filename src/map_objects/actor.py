from map_object import MapObject


class Actor(MapObject):

    def __init__(self, map, coord, name, color=None):

        MapObject.__init__(self)

        self.set_map(map)
        self.set_coord(coord)
        self.set_image(name)
        self.set_color(color)
