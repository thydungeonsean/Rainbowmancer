from src.state.ui.ability_icon import AbilityIcon


class Ability(object):

    def __init__(self, ability_id, inventory):

        self.active = False

        self.icon = AbilityIcon(self, ability_id, (0, 0))

        self.inventory = inventory

        self.panel = None
        self.panel_slot = None

        self.state = 0

    def initialize(self, panel, slot, coord):

        self.set_panel(panel)
        self.set_panel_slot(slot)
        self.icon.position(coord)

    def set_panel(self, panel):
        self.panel = panel

    def set_panel_slot(self, slot):
        self.panel_slot = slot