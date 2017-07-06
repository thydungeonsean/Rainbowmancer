from src.state.ui.ability_icon import AbilityIcon


class Ability(object):

    def __init__(self, ability_id, inventory):

        self.active = False

        self.icon = AbilityIcon(self, ability_id, (0, 0), color='red')

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

    def click(self):
        if self.state == 0:
            self.inventory.select_button(self.panel_slot)
            self.state = 1
        elif self.state == 1:
            self.inventory.deselect_button(self.panel_slot)
            self.state = 0
            self.reset_ability()

    def reset_ability(self):
        pass  # clear target and boost crystals etc.

    def activate(self):
        self.icon.activate_icon()

    def deactivate(self):
        self.icon.deactivate_icon()
