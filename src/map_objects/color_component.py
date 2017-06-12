

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
        self.state = None
        self.base_color = self.set_base_color(color)
        self.current_color = (0, 0, 0)
        #self.current_color = self.get_color(0)

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
            return self.reflected_color()
        else:
            return

    def reflected_color(self):

        point = self.owner.coord
        return self.owner.map.color_map.get_reflected_color(point)
