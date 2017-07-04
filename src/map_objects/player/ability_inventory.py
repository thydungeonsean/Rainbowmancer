

class AbilityInventory(object):

    def __init__(self, player, abilities=[]):

        self.player = player

        self.ability_list = abilities[:]
