from src.map_objects.bolt import Bolt
from src.map_objects.explosion import Explosion


class EffectTracker(object):

    def __init__(self, game):
        self.game = game

        self.effects = []

    def effects_clear(self):
        if self.effects:
            return False
        return True

    def add_effect(self, effect):

        self.effects.append(effect)

    def add_bolt(self, origin, target, color):
        bolt = Bolt(self, self.game.level, origin, target, color)
        self.add_effect(bolt)

    def add_explosion(self, point, color):
        explosion = Explosion(self, self.game.level, point, color)
        self.add_effect(explosion)

    def end_effect(self, effect):
        self.effects.remove(effect)

    def run(self):
        for effect in self.effects:
            effect.run()
