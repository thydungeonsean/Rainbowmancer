from src.image.tileset import TileSet


class ImageComponent(object):

    def __init__(self, owner, img_id):

        self.owner = owner
        self.tileset = TileSet('creature', img_id)

    @property
    def coord(self):
        return self.owner.coord

    def draw(self, surface, tick):

        frame = self.get_frame(tick)
        tile = self.tileset.get_tile_image(frame)
        tile.position(self.coord)
        tile.draw(surface)

    def get_frame(self, tick):
        if tick < 15:
            return 'a'
        elif tick < 30:
            return 'b'
        elif tick < 45:
            return 'a'
        else:
            return 'b'

