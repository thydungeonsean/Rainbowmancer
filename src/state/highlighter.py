import pygame


class Highlighter(object):

    def __init__(self, game):

        self.game = game

        self.active = True

    def draw(self, surface):

        if not self.active:
            return

        if self.game.pointer.coord is None:
            return

        x, y = self.game.pointer.coord

        pygame.draw.rect(surface, (255, 255, 255), ((x*16, y*24), (16, 24)), 1)
