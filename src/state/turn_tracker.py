

class TurnTracker(object):

    def __init__(self, game):
        self.game = game
        self.monster_list = None

    def run(self):
        self.monster_list = list(filter(lambda x: x.team == 'monster', self.game.objects))
        # sort monster list
        self.monster_list = sorted(self.monster_list, key=self.dist_to_player)

        remaining = self.monster_list[:]
        while remaining:
            for monster in remaining:
                if monster.turn_component.get_state() == 'ready':
                    monster.ai_component.run()

            remaining = filter(lambda x: x.turn_component.get_state() == 'delay', remaining)
            map(lambda x: x.turn_component.refresh(), remaining)

        map(lambda x: x.turn_component.refresh(), self.monster_list)

        self.game.end_monster_turn()

    def dist_to_player(self, obj):

        mx, my = obj.coord
        px, py = self.game.player.coord

        return abs(mx-px) + abs(my-py)

