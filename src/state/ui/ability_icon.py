from icon import Icon
from src.image.tileset import TileSet


class AbilityIcon(Icon):

    def __init__(self, ability, ability_id, coord, color='white'):

        self.ability = ability
        self.ready = True

        image = TileSet.get_icon_tiles().get_tile_image(ability_id)
        w = image.rect.w
        h = image.rect.h

        Icon.__init__(self, coord, w, h, image, color)

        self.glow = False
        self.tick = 0

    def click(self, point):

        if self.point_is_over(point) and self.ready:
            self.ability.click()
            return True
        return False

    def draw(self, surface, tick):

        if self.glow:

            color = self.color_component.get_boosted_color(self.color_component.ready_shade(), self.tick)
            self.tick += 1
            if self.tick > 59:
                self.tick = 0

        elif self.ready:
            color = self.color_component.ready_shade()

        else:
            color = self.color_component.inactive_shade()

        self.image.recolor(color)

        self.image.draw(surface)

    def activate_icon(self):
        self.ready = True

    def deactivate_icon(self):
        self.ready = False

    def boost_icon(self):
        self.glow = True

    def unboost_icon(self):
        self.glow = False
