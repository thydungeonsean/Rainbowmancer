from actor import Actor
from components.turn_component import TurnComponent
from components.ai_component import AIComponent


class Monster(Actor):

    def __init__(self, map, coord, name, color=None):

        Actor.__init__(self, map, coord, name, color)
        self.team = 'monster'
        self.turn_component = TurnComponent(self)
        self.set_ai(AIComponent(self))

