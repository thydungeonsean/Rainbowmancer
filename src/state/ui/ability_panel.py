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

        self.inventory = None

        self.ability_slots = {}
        self.ability_positions = self.set_ability_positions()

        self.initialize()

    def initialize(self):

        pass

    def load_player(self):

        self.inventory = self.ui.game.player.ability_inventory

        self.initialize()

    @staticmethod
    def set_ability_positions():

        ability_positions = {}

        for i in range(10):

            x = AbilityPanel.icon_x
            y = i * 32 + AbilityPanel.icon_margin

            ability_positions[i] = (x, y)

        return ability_positions
