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

    def get_color(self, tick):
        if self.mode == 'reflect':
            return self.reflected_color(tick)
        elif self.mode == 'generate':
            return self.generated_color(tick)

    def reflected_color(self, tick):

        point = self.owner.coord
        base = self.owner.map.color_map.get_reflected_color(point)
        if self.state == 'weak':
            return self.get_drained_color(base, tick)
        else:
            return base

    def generated_color(self, tick):

        base = hue_key[self.base_color][5]
        if self.state == 'weak':
            return self.get_drained_color(base, tick)

        affinity = self.get_affinity()
        if affinity is None:
            return base
        elif affinity == 'positive':
            return self.get_boosted_color(base, tick)
        elif affinity == 'negative':
            return self.get_drained_color(base, tick)

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
