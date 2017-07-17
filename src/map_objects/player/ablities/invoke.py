from ability import Ability


class Invoke(Ability):

    def __init__(self, inventory):

        Ability.__init__(self, 'invoke', inventory)

    def trigger_ability(self):

        print 'invoke'
