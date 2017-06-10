

class LightSource(object):

    def __init__(self, coord, color, strength):

        self.coord = coord
        self.color = color
        self.strength = strength

    def move(self, new):
        self.coord = new
