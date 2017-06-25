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

    def set_stats(self, stats):
        self.stat_component = stats

    def get_move_component(self, color):

        return MoveComponent(self, self.map, color)

    def bump(self, target):
        target.on_bump()
        if self.stat_component is not None:
            if self.target_is_enemy(target) and target.stat_component is not None:
                self.attack(target)

    def on_bump(self):
        self.color_component.flash()

    def attack(self, target):
        pass

    def target_is_enemy(self, target):

        return target.team != self.team
