from src.color.color_palette import hue_key, hue_interaction, boost_color, drain_color


class ColorComponent(object):

    key = {
        0: 'white',
        1: 'red',
        2: 'green',
        3: 'blue',
        4: 'yellow',
        5: 'purple',
        6: 'cyan'
    }

    encode = {v: k for k, v in key.iteritems()}

    def __init__(self, owner, color=None):

        self.owner = owner
        self.mode = self.set_color_mode(color)
        self.state = None  # TODO maybe state should be property referring to owner's state
        self.base_color = self.set_base_color(color)
        self.current_color = (0, 0, 0)
        self.flashes = []

    @property
    def current_object_hue(self):
        if self.mode == 'generate':
            return self.base_color
        elif self.mode == 'reflect':
            return self.get_current_tile_hue()

    def hue_interaction(self, target):
        return hue_interaction(self.current_object_hue, target.owner.color_component.current_object_hue)

    @staticmethod
    def set_color_mode(color):
        if color is None:
            return 'reflect'
        else:
            return 'generate'

    @staticmethod
    def set_base_color(color):
        if color is None:
            return 0
        return ColorComponent.encode[color]

    def get_base_color(self):
        return hue_key[self.base_color][5]

    def ready_shade(self):
        return hue_key[self.base_color][5]

    def inactive_shade(self):
        return hue_key[self.base_color][1]

    def get_color(self, tick):

        if self.flashes:
            flash = self.flashes[0].get_color()
            if flash is not None:
                return flash

        if self.mode == 'reflect':
            return self.reflected_color(tick)
        elif self.mode == 'generate':
            return self.generated_color(tick)

    def get_current_tile_hue(self):
        return self.owner.map.color_map.get_tile_hue(self.owner.coord)

    def reflected_color(self, tick):

        point = self.owner.coord
        base = self.owner.map.color_map.get_reflected_color(point)
        if self.state == 'weak':
            return self.get_drained_color(base, tick)
        else:
            return base

    def generated_color(self, tick):

        base = self.get_base_color()
        if self.state == 'weak':
            return self.get_drained_color(base, tick)

        affinity = self.get_affinity()
        if affinity in (None, 'strong_against'):
            return self.get_base_color()
        elif affinity == 'boosted':
            return self.get_boosted_color(base, tick)
        elif affinity == 'weak_against':
            return self.get_drained_color(base, tick)

    def flash(self):
        self.flashes.append(Flash(self))

    def get_affinity(self):
        point = self.owner.coord
        tile_hue = self.owner.map.color_map.get_tile_hue(point)
        return hue_interaction(self.base_color, tile_hue)

    @staticmethod
    def get_boosted_color(base, tick):
        mod = 10
        if tick < 15 or 30 <= tick < 45:
            boost_mod = (tick % 15) * mod
        else:
            boost_mod = 15 * mod - (tick % 15) * mod
        return boost_color(base, boost_mod)

    @staticmethod
    def get_drained_color(base, tick):
        mod = 15
        if tick < 15 or 30 <= tick < 45:
            drain_mod = (tick % 15) * mod
        else:
            drain_mod = 15 * mod - (tick % 15) * mod

        return drain_color(base, drain_mod)

    # @staticmethod
    # def get_drained_color_slow(base, tick):
    #     mod = 10
    #     if tick < 30:
    #         drain_mod = (tick % 30) * mod
    #     else:
    #         drain_mod = 30 * mod - (tick % 30) * mod
    #
    #     return drain_color(base, drain_mod)


class Flash(object):

    # seq = (0, 1, 1, 0, 0, 1, 1, 0, 0)
    seq = (0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0)

    def __init__(self, color_component):
        self.color_component = color_component
        self.tick = 0

        self.flash_color = self.set_flash_color()

    def get_color(self):

        self.tick += 1
        if self.tick >= len(Flash.seq):
            self.end_flash()
            return None

        if Flash.seq[self.tick] == 1:
            return self.flash_color
        else:
            return None

    def set_flash_color(self):

        if self.color_component.mode == 'generate':
            if self.color_component.base_color == 0:
                return hue_key[1][5]  # red flash
            else:
                return hue_key[0][5]  # white flash
        elif self.color_component.mode == 'reflect':
            if self.color_component.get_current_tile_hue() == 0:
                return hue_key[1][5]  # red flash
            else:
                return hue_key[0][5]

    def end_flash(self):
        self.color_component.flashes.remove(self)

