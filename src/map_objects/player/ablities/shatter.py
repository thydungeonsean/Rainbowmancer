from ability import Ability


class Shatter(Ability):

    def __init__(self, inventory):

        Ability.__init__(self, 'shatter', inventory)
        self.restrict_terrain = True
        self.target_terrain = {1, 3, 4, 5, 8}

    def trigger_ability(self):

        print 'shattered'
