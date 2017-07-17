from ability import Ability


class Block(Ability):

    def __init__(self, inventory):

        Ability.__init__(self, 'block', inventory)
        self.not_enemy = True
        self.restrict_terrain = True
        self.target_terrain = {0}

    def trigger_ability(self):

        print 'block'
