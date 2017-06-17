

class LightComponent(object):

    def __init__(self, owner, map, color, strength):

        self.owner = owner
        self.map = map

        self.source = map.color_source_generator.get_color_source(self.coord, color, strength)

    @property
    def coord(self):
        return self.owner.coord

    def move(self, new):
        self.source.move(new)

    def kill(self):
        self.source.kill()
