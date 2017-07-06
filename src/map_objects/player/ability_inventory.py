from ablities.ability_collection import *


class AbilityInventory(object):

    def __init__(self, player, abilities=('bolt', 'bind', 'ray')):

        self.player = player

        self.ability_list = []

        self.initialize_abilities(abilities[:])

    def initialize_abilities(self, ability_ids):

        for ability_id in ability_ids:
            self.ability_list.append(new_ability(ability_id, self))

    def add_ability(self, new_id):
        pass

    def activate_ability(self, ability_id):
        pass

    def select_button(self, slot):
        other_abilities = filter(lambda a: a.panel_slot != slot, self.ability_list)
        map(lambda a: a.deactivate(), other_abilities)

    def deselect_button(self, slot):
        map(lambda a: a.activate(), self.ability_list)
