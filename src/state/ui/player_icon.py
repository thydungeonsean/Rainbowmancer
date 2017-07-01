from icon import Icon


class PlayerIcon(Icon):

    def __init__(self, player, coord):

        Icon.__init__(self, coord, 16, 24, None)
        self.player = player

    def draw(self, surface, tick):

        self.player.image_component.draw_at_coord(surface, tick, self.coord)
