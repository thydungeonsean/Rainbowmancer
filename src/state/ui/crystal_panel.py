from src.image.panel_border import PanelBorder


class CrystalPanel(object):

    def __init__(self, ui):

        self.ui = ui

        self.crystal_inventory = None
        self.border = PanelBorder(pix_w=240, pix_h=720)
        self.border.rect.topright = 960, 0

    def draw(self, surface):
        self.border.draw(surface)
