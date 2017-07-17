from ablities.ability_collection import *


class AbilityInventory(object):

    def __init__(self, player, abilities=('bolt', 'bind', 'ray', 'summon', 'invoke', 'imbue', 'shatter', 'block')):

        self.player = player

        self.ability_list = []

        self.initialize_abilities(abilities[:])

        self.hue_code = 0

    def initialize_abilities(self, ability_ids):

        for ability_id in ability_ids:
            self.ability_list.append(new_ability(ability_id, self))

    def add_ability(self, new_id):
        pass

    def select_ability(self, selection, slot):
        self.player.map.game.set_active_ability(selection)
        self.player.crystal_inventory.activate_crystals(selection)

        selection.compute_valid_targets()

        other_abilities = filter(lambda a: a.panel_slot != slot, self.ability_list)
        map(lambda a: a.deactivate(), other_abilities)
        self.player.map.game.highlighter.activate()

    def deselect_ability(self):
        self.player.map.game.clear_active_ability()
        map(lambda a: a.activate(), self.ability_list)
        self.player.crystal_inventory.deactivate_crystals()
        self.player.map.game.highlighter.deactivate()

    def cancel_ability(self):
        self.deselect_ability()
        map(lambda a: a.reset_ability(), self.ability_list)

    def update(self):  # called at start of each player turn - updates color if necessary

        if self.hue_code != self.player.color_component.current_object_hue_code:
            self.hue_code = self.player.color_component.current_object_hue_code
            map(lambda a: a.set_hue(self.hue_code), self.ability_list)

