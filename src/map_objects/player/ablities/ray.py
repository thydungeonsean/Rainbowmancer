from ability import Ability


class Ray(Ability):

    def __init__(self, inventory):

        Ability.__init__(self, 'ray', inventory)
        self.not_self = True

    def trigger_ability(self):

        print 'ray fired'
