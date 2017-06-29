

class CrystalInventory(object):

    colors = ('red', 'green', 'blue', 'yellow', 'purple', 'cyan', 'white')

    default_num = {
        'red': 1,
        'green': 1,
        'blue': 1,
        'yellow': 0,
        'purple': 0,
        'cyan': 0,
        'white': 0
    }

    default_level = {
        'red': 1,
        'green': 1,
        'blue': 1,
        'yellow': 0,
        'purple': 0,
        'cyan': 0,
        'white': 0
    }

    def __init__(self, **kwargs):
        # init the inventory with keywords for number of the color crystals eg"red"
        # and level of the color eg "red_level"

        self.crystal_num = {}
        self.crystal_level = {}

        for color in CrystalInventory.colors:
            self.crystal_num[color] = kwargs.get(color, CrystalInventory.default_num[color])
            self.crystal_num[color] = kwargs.get(''.join((color, '_level')), CrystalInventory.default_level[color])

    def spend_crystal(self, color):
        self.crystal_num[color] -= 1
        assert self.crystal_num[color] > 0

    def gain_crystal(self, color):
        self.crystal_num[color] += 1
        if self.crystal_num[color] > 10:  # max inventory limit
            self.crystal_num[color] = 10