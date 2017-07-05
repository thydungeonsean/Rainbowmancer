from icon import Icon
from src.image.tileset import TileSet


class AbilityIcon(Icon):

    def __init__(self, ability, ability_id, coord):

        self.ability = ability

        image = TileSet.get_icon_tiles().get_tile_image(ability_id)
        w = image.rect.w
        h = image.rect.h

        Icon.__init__(self, coord, w, h, image)
