

class MoveComponent(object):

    def __init__(self, owner, map, color=None):

        self.owner = owner
        self.map = map
        self.color = color

    def can_move(self, point):

        if self.map.terrain_map.get_tile(point) in (1, 2, 4, 8):
            # cannot move through wall, stalagtite, or brazier
            return False

        blocking_objects = filter(lambda x: x.coord == point, self.map.game.objects)
        if blocking_objects:  # there is an object on point
            for obj in blocking_objects:
                if obj.blocks:
                    return False

        # for monsters, cannot move into opposed color

        return True

    def can_bump(self, point):

        blocking_objects = filter(lambda x: x.coord == point, self.map.game.objects)

        for obj in blocking_objects:
            if obj.blocks:

                # bump object if object team doesn't match yours
                if self.opposed_team(obj):
                    return True, obj
                elif obj.object_type == 'door':  # monsters can open doors
                    return True, obj

        return False, None

    def opposed_team(self, obj):
        return obj.team is not None and obj.team != self.owner.team