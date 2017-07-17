import pygame


class Highlighter(object):

    def __init__(self, game):

        self.game = game

        self.active = False
        self.ability = None

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def set_active_ability(self, ability):
        self.ability = ability
        self.activate()

    def draw(self, surface):

        if not self.active:
            return

        if self.game.pointer.coord is None:
            return

        x, y = self.game.pointer.coord
        color = self.get_pointer_color((x, y))
        pygame.draw.rect(surface, color, ((x*16, y*24), (16, 24)), 1)

    def get_pointer_color(self, (x, y)):

        if self.game.active_ability is not None:
            ability = self.game.active_ability
            if (x, y) in ability.valid_targets:
                return 40, 255, 20

        return 255, 255, 255
