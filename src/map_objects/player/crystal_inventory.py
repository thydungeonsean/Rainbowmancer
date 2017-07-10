from src.color.color_palette import hue_ability_affinities, hue_names


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

    def __init__(self, player, **kwargs):
        # init the inventory with keywords for number of the color crystals eg"red"
        # and level of the color eg "red_level"

        self.player = player

        self.panel = None

        self.crystal_num = {}
        self.crystal_level = {}
        self.crystal_icon_active = {k: False for k in CrystalInventory.colors}

        for color in CrystalInventory.colors:
            self.crystal_num[color] = kwargs.get(color, CrystalInventory.default_num[color])
            self.crystal_level[color] = kwargs.get(''.join((color, '_level')), CrystalInventory.default_level[color])

    def set_panel(self, panel):
        self.panel = panel

    def spend_crystal(self, color):
        self.crystal_num[color] -= 1
        assert self.crystal_num[color] > 0
        self.update_display()

    def gain_crystal(self, color):
        self.crystal_num[color] += 1
        if self.crystal_num[color] > 10:  # max inventory limit
            self.crystal_num[color] = 10
        self.update_display()

    def lower_level(self, color):
        self.crystal_level[color] -= 1
        assert self.crystal_level[color] >= 0
        self.update_display()

    def raise_level(self, color):
        self.crystal_level[color] += 1
        if self.crystal_level[color] > 10:  # max inventory limit
            self.crystal_level[color] = 10
        self.update_display()

    def update_display(self):

        self.player.map.game.ui.panels['crystal'].change()

    def activate_crystals(self, ability):

        affinities = hue_ability_affinities[ability.hue]  # a set of hue codes for valid color crystals

        for code in affinities:
            color_name = hue_names[code]
            # if this color crystal has enough quantity for ability
            self.crystal_icon_active[color_name] = True

        self.update_display()

    def deactivate_crystals(self):
        for c in CrystalInventory.colors:
            self.crystal_icon_active[c] = False
        self.update_display()
