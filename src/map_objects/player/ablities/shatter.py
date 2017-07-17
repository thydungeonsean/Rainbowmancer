from ability import Ability


class Shatter(Ability):

    def __init__(self, inventory):

        Ability.__init__(self, 'shatter', inventory)

    def is_valid_target(self, coord):

        pass

    def trigger_ability(self):

        print 'shattered'
