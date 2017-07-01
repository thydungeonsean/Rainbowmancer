from panel import Panel
from src.image.tileset import TileSet


class AbilityPanel(Panel):
    w = 240
    h = 360

    x = 960 - w
    y = 360
    coord = (x, y)

    icon_x = 16
    icon_margin = 20

    def __init__(self, ui):
        pix_w = AbilityPanel.w
        pix_h = AbilityPanel.h
        coord = AbilityPanel.coord

        Panel.__init__(self, ui, pix_w, pix_h, coord=coord)

        self.ability_slots = {}
        self.ability_positions = self.set_ability_positions()

        self.initialize()

    def initialize(self):

        pass

    @staticmethod
    def set_ability_positions():

        ability = {}

        for i in range(10):

            x = AbilityPanel.icon_x
            y = i * 32 + AbilityPanel.icon_margin

            ability[i] = (x, y)

        return ability