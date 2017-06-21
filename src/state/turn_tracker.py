

class TurnTracker(object):

    def __init__(self, game):
        self.game = game
        self.monster_list = None

    def run(self):
        self.monster_list = list(filter(lambda x: x.team == 'monster', self.game.objects))

        # sort monster list
        remaining = self.monster_list
        while remaining:
            for monster in remaining:
                if monster.turn_component.get_state() == 'ready':
                    monster.ai_component.run()

            remaining = filter(lambda x: x.turn_component.get_state() == 'delay', remaining)
            map(lambda x: x.turn_component.refresh(), remaining)
            for x in remaining:
                print x.turn_component.get_state()

        map(lambda x: x.turn_component.refresh(), self.monster_list)

        self.game.end_monster_turn()

