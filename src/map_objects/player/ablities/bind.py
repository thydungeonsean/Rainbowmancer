from ability import Ability


class Bind(Ability):

    def __init__(self, inventory):

        Ability.__init__(self, 'bind', inventory)

    def is_valid_target(self, coord):

        pass

    def trigger_ability(self):

        print 'bound'
