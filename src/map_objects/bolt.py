from effect import Effect
from components.image_component import EffectImageComponent
from components.light_component import LightComponent


class Bolt(Effect):

    def __init__(self, effect_tracker, map, origin, target, color):

        self.axis = 'x'
        self.mod = 1

        self.target = target
        self.base_color = color

        self.tick = 0

        Effect.__init__(self, effect_tracker)
        self.set_map(map)
        self.set_coord(self.get_initial_coord(origin, target))
        self.set_color(color)
        self.set_image()
        self.set_light(LightComponent(self, map, color, 3))

        self.blocks = False

    def set_image(self):
        self.image_component = EffectImageComponent(self, 'bolt', tile_set='projectile')

    def get_initial_coord(self, origin, target):

        ox, oy = origin.coord
        tx, ty = target.coord

        xdiff = tx - ox
        ydiff = ty - oy

        x = ox
        y = oy

        if xdiff != 0:
            self.axis = 'x'
            if xdiff < 0:
                x = ox - 1
                self.mod = -1
            elif xdiff > 0:
                x = ox + 1
                self.mod = 1

        if ydiff != 0:
            self.axis = 'y'
            if ydiff < 0:
                y = oy - 1
                self.mod = -1
            elif ydiff > 0:
                y = oy + 1
                self.mod = 1

        return x, y

    def run(self):

        self.tick += 1

        if self.tick % 5 == 0:
            self.update_effect()

    def update_effect(self):
        if self.coord == self.target.coord:
            self.effect_tracker.end_effect(self)
            self.light_component.kill()
            self.effect_tracker.add_explosion(self.coord, self.base_color)

        x, y = self.coord
        if self.axis == 'x':
            new = (x+self.mod, y)
        else:
            new = (x, y+self.mod)
        self.move(new)
        self.image_component.change_frame()
