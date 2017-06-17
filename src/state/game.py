import pygame
from pygame.locals import *
from src.map.mapgen.master_map_gen import LevelGen


class Game(object):

    FPS = 60

    def __init__(self, player_key):

        self.level = None
        self.player = None
        self.player_key = player_key
        self.objects = []

        self.clock = pygame.time.Clock()
        self.tick = 0

        self.sub_screen = pygame.Surface((400*2, 300*2))

        self.turn = 'player'

    def load_level(self):

        self.level = LevelGen.generate_level(self)

        self.player = self.level.map_object_generator.add_player(self.player_key, self.level.player_start)

    def increment_tick(self):
        self.tick += 1
        if self.tick > 60:
            self.tick = 0

    def draw(self):

        screen = pygame.display.get_surface()
        sw = self.sub_screen.get_width()
        sh = self.sub_screen.get_height()

        self.level.map_image.draw(self.sub_screen, self.tick)

        for object in self.objects:
            object.draw(self.sub_screen, self.tick)

        # pygame.transform.scale(self.sub_screen, (sw*2, sh*2), screen)
        screen.blit(self.sub_screen, self.sub_screen.get_rect())

    def handle_input(self):

        for event in pygame.event.get():

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return True

                if self.turn == 'player':
                    if event.key == K_UP:
                        self.player.move_player('up')
                    elif event.key == K_DOWN:
                        self.player.move_player('down')
                    elif event.key == K_RIGHT:
                        self.player.move_player('right')
                    elif event.key == K_LEFT:
                        self.player.move_player('left')

        return False

    def run(self):

        self.level.redraw_manager.run()

        # run ai
        # run effects

    def main(self):

        while True:

            if self.handle_input():
                break

            self.run()

            self.draw()
            pygame.display.update()

            self.clock.tick(Game.FPS)
            self.increment_tick()
            # print self.clock.get_fps()
