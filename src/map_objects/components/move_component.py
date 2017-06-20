

class MoveComponent(object):

    def __init__(self, owner, map, color=None):

        self.owner = owner
        self.map = map
        self.color = color

    def can_move(self, point):

        if self.map.terrain_map.get_tile(point) in (1, 2, 4, 8):
            # cannot move through wall, stalagtite, or brazier
            return False

        objects = self.map.game.objects
        blocking_objects = filter(lambda x: x.coord == point, objects)
        if blocking_objects:
            for object in blocking_objects:
                if object.blocks:
                    self.owner.bump(object)
                    print self.owner.team + ' bump ' + str(object.team)
                    return False

        return True

        # for monsters, cannot move into opposed color
