from ability import Ability


class Bind(Ability):

    def __init__(self, inventory):

        Ability.__init__(self, 'bind', inventory)
        self.restrict_terrain = True
        self.target_terrain = {8}

    def trigger_ability(self):

        print 'bound'
