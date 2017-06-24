from map_object import MapObject


class Effect(MapObject):

    def __init__(self, effect_tracker):
        MapObject.__init__(self)
        self.effect_tracker = effect_tracker

    def run(self):
        pass
