from src.image.tileset import TileSet


class ImageComponent(object):

    def __init__(self, owner, img_id, tile_set='creature'):

        self.owner = owner
        self.tileset = TileSet(tile_set, img_id)

    @property
    def coord(self):
        return self.owner.coord

    def draw(self, surface, tick):

        frame = self.get_frame(tick)
        tile = self.tileset.get_tile_image(frame)

        color = self.owner.color_component.get_color(tick)
        tile.recolor(color)

        tile.position(self.coord)
        tile.draw(surface)

    def draw_at_coord(self, surface, tick, coord):

        frame = self.get_frame(tick)
        tile = self.tileset.get_tile_image(frame)

        color = self.owner.color_component.get_color(tick)
        tile.recolor(color)

        tile.position_pixel(coord)
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


class EffectImageComponent(ImageComponent):

    def __init__(self, owner, img_id, tile_set='effect'):
        ImageComponent.__init__(self, owner, img_id, tile_set=tile_set)
        self.frame = 'a'

    def get_frame(self, tick):
        return self.frame

    def change_frame(self):
        if self.frame == 'a':
            self.frame = 'b'
        else:
            self.frame = 'a'

