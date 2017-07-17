from ability import Ability


class Block(Ability):

    def __init__(self, inventory):

        Ability.__init__(self, 'block', inventory)

    def is_valid_target(self, coord):

        player = self.inventory.player.coord

        return coord == player

    def trigger_ability(self):

        print 'block'
