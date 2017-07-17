from ability import Ability


class Summon(Ability):

    def __init__(self, inventory):

        Ability.__init__(self, 'summon', inventory)
        self.not_self = True
        self.not_enemy = True
        self.restrict_terrain = True
        self.target_terrain = {0, 1, 2, 3, 4, 7, 8}

    def trigger_ability(self):

        print 'summoned'
