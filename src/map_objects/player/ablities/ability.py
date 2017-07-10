from src.state.ui.ability_icon import AbilityIcon
from pygame.locals import *
from boost_slot import BoostSlot


class Ability(object):

    valid_keys = (K_UP, K_DOWN, K_RIGHT, K_LEFT, K_SPACE)

    def __init__(self, ability_id, inventory):

        self.icon = AbilityIcon(self, ability_id, (0, 0), color='white')
        self.inventory = inventory
        self.panel = None
        self.panel_slot = None

        self.active = False
        self.state = 0

        self.hue = 0  # hue code of player - determines ability effect and what kind of boosts available

        self.needs_boost = True  # some abilities need crystal boost to trigger
        self.cost = 1  # cost of crystal boost

        self.boost_slot = BoostSlot(self)

        self.valid_targets = set()
        self.target = None

        # need functions for determining valid targets

    def initialize(self, panel, slot, coord):

        self.set_panel(panel)
        self.set_panel_slot(slot)
        self.icon.position(coord)

    def set_panel(self, panel):
        self.panel = panel

    def set_panel_slot(self, slot):
        self.panel_slot = slot

    def click_icon(self):
        if self.state == 0:
            self.inventory.select_button(self, self.panel_slot)
            self.state = 1
            self.icon.boost_icon()
        elif self.state == 1:
            self.inventory.deselect_button()
            self.state = 0
            self.reset_ability()

    def reset_ability(self):
        self.state = 0
        self.icon.unboost_icon()
        self.boost_slot.clear_color()
        self.clear_target()

    def activate(self):
        self.icon.activate_icon()

    def deactivate(self):
        self.icon.deactivate_icon()

    def handle_player_input(self, pointer, event):
        pointer.switch_keys_mode()
        if event.key == K_UP:
            pointer.move_up()
        elif event.key == K_DOWN:
            pointer.move_down()
        elif event.key == K_RIGHT:
            pointer.move_right()
        elif event.key == K_LEFT:
            pointer.move_left()
        elif event.key == K_SPACE:
            self.click_map(pointer.coord)

    def set_hue(self, hue_code):
        self.icon.color_component.generate_hue(hue_code)
        self.hue = hue_code

    def clicked_crystal(self, color):

        self.boost_slot.crystal_click(color)

    def cast(self):

        if self.needs_boost and self.boost_slot.boost_color is None:
            print 'needs boost'
            return False  # needs a boost - feedback?

        if self.target is None:
            print 'no target'
            return False  # needs a target

        self.trigger_ability()

    def click_map(self, pos):
        print pos
        self.set_target(pos)
        self.cast()

    def set_target(self, target):

        # if target is valid

        self.target = target

    def clear_target(self):
        self.target = None

    def trigger_ability(self):

        print 'ability fired'
