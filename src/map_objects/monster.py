from actor import Actor
from components.turn_component import TurnComponent
from components.ai_component import AIComponent
from components.stat_component import StatComponent


class Monster(Actor):

    def __init__(self, map, coord, name, color=None):

        Actor.__init__(self, map, coord, name, color)
        self.team = 'monster'
        self.object_type = 'monster'
        self.turn_component = TurnComponent(self)
        self.set_ai(AIComponent(self))
        self.set_stats(StatComponent(self))



