

# for keeping track of actor's position in the turn tracker

class TurnComponent(object):

    states = {
        0: 'ready',
        1: 'taken',
        2: 'delay'
    }

    def __init__(self, owner):

        self.owner = owner

        self.state = 0

    def get_state(self):
        return TurnComponent.states[self.state]

    def refresh(self):
        self.state = 0

    def delay(self):
        self.state = 2

    def take_turn(self):
        self.state = 1
