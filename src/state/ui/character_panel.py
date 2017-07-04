from panel import Panel
from player_icon import PlayerIcon
from src.image.tileset import TileSet


class CharacterPanel(Panel):

    w = 240
    h = 120

    x = 960 - w
    y = 0
    coord = (x, y)

    char_x = (w - 32) / 2 + 8
    char_y = h - 48

    def __init__(self, ui):

        pix_w = CharacterPanel.w
        pix_h = CharacterPanel.h
        coord = CharacterPanel.coord

        Panel.__init__(self, ui, pix_w, pix_h, coord=coord)

        self.player = None

    def load_player(self):

        self.player = self.ui.game.player

        self.initialize()

    def initialize(self):

        x = CharacterPanel.char_x + self.x
        y = CharacterPanel.char_y + self.y
        player_icon = PlayerIcon(self.player, (x, y))

        self.add_element(player_icon)

        self.draw_hearts()

    def update(self):
        self.needs_update = False

        self.border.draw(self.surface)
        self.draw_hearts()

    def draw_hearts(self):

        max = min((self.player.stat_component.max_health, 24))
        hp = self.player.stat_component.health

        full = TileSet.get_ui_tiles().get_tile_image('full_heart')
        empty = TileSet.get_ui_tiles().get_tile_image('empty_heart')

        margins = {}

        if max > 8:
            row_break = max / 2 + max % 2
            two_rows = True
            margins = {
                1: self.get_margin(row_break),
                2: self.get_margin(max - row_break)
            }
        else:
            two_rows = False
            margins[1] = self.get_margin(max)

        for i in range(max):

            if i < hp:
                tile = full
            else:
                tile = empty

            if not two_rows:

                x = margins[1] + i * 16
                y = 24 + 12
                tile.position_pixel((x, y))

            else:
                if i < row_break:
                    y = 24
                    x = margins[1] + i * 16
                else:
                    y = 48
                    x = margins[2] + (i - row_break) * 16
                tile.position_pixel((x, y))


            tile.draw(self.surface)

    @staticmethod
    def get_margin(length):

        cls = CharacterPanel

        return (cls.w - (length * 16)) / 2
