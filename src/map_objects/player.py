from actor import Actor
from components.stat_component import StatComponent
from crystal_inventory import CrystalInventory


class Player(Actor):

    move_code = {
        'up': (0, -1),
        'down': (0, 1),
        'right': (1, 0),
        'left': (-1, 0)
    }

    def __init__(self, coord, player_key):

        Actor.__init__(self, None, coord, player_key, color=None)
        self.team = 'player'
        self.object_type = 'player'

        self.mode = 'move'

        self.set_stats(StatComponent(self, health=20))

        self.crystal_inventory = CrystalInventory()

    def initialize(self, level):
        self.set_map(level)
        self.move_component.map = level

    def move_player(self, code):

        if self.mode == 'bolt':
            can_fire, target = self.check_bolt_target(code)
            if can_fire:
                self.fire_bolt(target)
                return

        mx, my = Player.move_code[code]
        new = self.coord[0]+mx, self.coord[1]+my

        can_move = self.move_component.can_move(new)
        can_bump, target = self.move_component.can_bump(new)

        if can_move:
            self.move(new)
            self.map.fov_map.recompute_fov()
            self.map.path_finding_map.compute()
            self.map.game.end_player_turn()
        elif can_bump:
            self.bump(target)
            self.map.game.end_player_turn()

    def fire_bolt(self, target):

        print 'shoot at ' + str(target)
        self.stat_component.fire_bolt(target.stat_component)
        self.map.game.end_player_turn()
        self.map.game.effect_tracker.add_bolt(self, target, 'red')

    def check_bolt_target(self, code):

        coord_seq = self.get_row_sequence(code)
        for coord in coord_seq:
            is_target, target = self.coord_is_fire_target(coord)
            if is_target:
                return True, target

            if self.coord_blocks_fire(coord):
                break

        return False, None

    def get_row_sequence(self, code):

        sx, sy = self.coord

        if code in ('up', 'down'):
            axis = 'y'
        else:
            axis = 'x'

        if code in ('up', 'left'):
            mod = -1
        else:
            mod = 1

        row = []

        for m in range(1, 8):
            if axis == 'x':
                row.append((sx+(m*mod), sy))
            elif axis == 'y':
                row.append((sx, sy+(m*mod)))

        return row

    def coord_is_fire_target(self, coord):

        targets = filter(lambda x: x.coord == coord and x.team == 'monster', self.map.game.objects)
        if targets:
            return True, targets.pop()
        return False, None

    def coord_blocks_fire(self, coord):

        if self.map.terrain_map.get_tile(coord) not in (0, 3):  # can only shoot over floor and open doors
            return True
        if not self.map.fov_map.point_is_visible(coord):  # can't shoot beyond fov
            return True
        return not self.map.fov_map.point_transparent(coord)  # can't shoot beyond objects that block sight

    def trigger_attack_effects(self, target):
        target.ai_component.stun()

