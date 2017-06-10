

class MapObject(object):

    def __init__(self):

        self.coord = None

        self.light_component = None

    def move(self, new):
        self.coord = new
        if self.light_component is not None:
            self.light_component.move(new)
