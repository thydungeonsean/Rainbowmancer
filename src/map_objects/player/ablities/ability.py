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
            self.inventory.select_ability(self, self.panel_slot)
            self.state = 1
            self.icon.boost_icon()
        elif self.state == 1:
            self.inventory.deselect_ability()
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

    def set_hue_to_inventory_hue(self):
        hue = self.inventory.hue_code
        self.set_hue(hue)

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
        if target in self.valid_targets:

            self.target = target
        else:
            self.clear_target()

    def clear_target(self):
        self.target = None

    def trigger_ability(self):

        print 'ability fired'

    def compute_valid_targets(self):
        all_coords = self.inventory.player.map.terrain_map.all_points
        valid_targets = set(filter(self.is_valid_target, all_coords))

        self.valid_targets = valid_targets

    def is_valid_target(self, coord):  # tune this function for different targeting schemes

        level = self.inventory.player.map

        # if needs fov, filter by in fov
        if not level.fov_map.point_is_visible(coord):
            return False

        # if only target enemies - restrict to enemy coords


        # if only target certain terrain types filter terrain map
        valid_terrain = (0, 3, 5, 6, 8)



        return True
