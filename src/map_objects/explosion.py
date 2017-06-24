from effect import Effect
from components.image_component import EffectImageComponent
from components.light_component import LightComponent


class Explosion(Effect):

    def __init__(self, effect_tracker, map, coord, color):

        Effect.__init__(self, effect_tracker)
        self.set_map(map)
        self.set_coord(coord)
        self.set_color(color)
        self.set_light(LightComponent(self, map, color, 5))

        self.set_image()

        self.tick = 0
        self.frame = '1'
        self.image_component.frame = self.frame

    def set_image(self):
        self.image_component = EffectImageComponent(self, 'explode')

    def change_frame(self, frame):
        self.image_component.frame = frame

    def run(self):

        self.tick += 1

        if self.tick % 3 == 0:
            self.update_effect()

    def update_effect(self):

        if self.frame == '5':
            self.effect_tracker.end_effect(self)
            self.light_component.kill()

        self.frame = str(int(self.frame)+1)
        self.change_frame(self.frame)
