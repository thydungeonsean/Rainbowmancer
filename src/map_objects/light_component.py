from src.map.light_source import LightSource


class LightComponent(object):

    def __init__(self, owner, map, color, strength):

        self.owner = owner
        self.map = map
        self.coord = owner.coord

        self.source = LightSource(self.coord, color, strength)

    def move(self, new):
        self.source.move(new)
