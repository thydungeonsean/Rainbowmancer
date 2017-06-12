

class ColorSource(object):

    def __init__(self, master, coord, color, strength):

        self.master = master

        self.coord = coord
        self.color = color
        self.strength = strength

    def move(self, new):
        self.coord = new
        self.master.move_source(self)

    def kill(self):
        self.master.remove_source(self)


class ColorSourceGen(object):

    def __init__(self):

        self.color_map = None

    def set_color_map(self, color_map):
        self.color_map = color_map

    def get_color_source(self, coord, color, strength):

        assert self.color_map is not None

        s = ColorSource(self.color_map, coord, color, strength)
        self.color_map.add_source(s)
        return s
