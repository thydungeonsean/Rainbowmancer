from map_object import MapObject
from components.move_component import MoveComponent


class Actor(MapObject):

    def __init__(self, map, coord, name, color=None):

        MapObject.__init__(self)

        self.set_map(map)
        self.set_coord(coord)
        self.set_image(name)
        self.set_color(color)
        self.set_move(self.get_move_component(color))

        self.object_type = 'actor'

    def get_move_component(self, color):

        return MoveComponent(self, self.map, color)

    def bump(self, target):
        target.on_bump()

    def on_bump(self):
        self.color_component.flash()
