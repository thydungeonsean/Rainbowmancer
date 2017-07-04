from src.image.panel_border import PanelBorder
import pygame


class Panel(object):

    def __init__(self, ui, pix_w, pix_h, coord=(0, 0)):

        self.ui = ui

        self.w = pix_w
        self.h = pix_h

        self.border = PanelBorder(pix_w=pix_w, pix_h=pix_h)

        self.needs_update = True

        self.surface = pygame.Surface((pix_w, pix_h)).convert()
        self.rect = self.surface.get_rect()
        self.rect.topleft = coord

        self.border.draw(self.surface)

        self.coord = coord

        self.elements = []

    def update(self):
        # update surface or other
        self.needs_update = False

        self.border.draw(self.surface)

    def draw(self, surface, tick):

        if self.needs_update:
            self.update()
            surface.blit(self.surface, self.rect)

        for element in self.elements:
            element.draw(surface, tick)

    def point_is_over(self, (x, y)):

        cx, cy = self.coord
        return cx <= x < cx + self.w and cy <= y < cy + self.h

    def click(self, (x, y)):
        if self.point_is_over((x, y)):
            for e in self.elements:
                click = e.click((x, y))
                if click:
                    return True
        return False

    def right_click(self, (x, y)):
        if self.point_is_over((x, y)):
            for e in self.elements:
                click = e.right_click((x, y))
                if click:
                    return True
        return False

    def add_element(self, element):
        self.needs_update = True
        self.elements.append(element)

    def change(self):
        self.needs_update = True
