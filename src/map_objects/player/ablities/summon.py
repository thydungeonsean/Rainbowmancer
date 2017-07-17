from ability import Ability


class Summon(Ability):

    def __init__(self, inventory):

        Ability.__init__(self, 'summon', inventory)

    def is_valid_target(self, coord):

        pass

    def trigger_ability(self):

        print 'summoned'
