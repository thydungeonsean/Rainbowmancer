import pygame
from pygame.locals import *
from src.map.mapgen.level_gen import LevelGen
from turn_tracker import TurnTracker


class Game(object):

    FPS = 60

    def __init__(self, player_key):

        self.level = None
        self.player = None
        self.player_key = player_key
        self.objects = []

        self.turn_tracker = TurnTracker(self)
        self.turn = 'player'

        self.clock = pygame.time.Clock()
        self.tick = 0

        self.sub_screen = pygame.Surface((400*2, 300*2))

    def load_level(self):

        self.level = LevelGen.generate_level(self)

        self.player = self.level.map_object_generator.add_player(self.player_key, self.level.player_start)
        self.level.load_player(self.player)

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
                    elif event.key == K_SPACE:
                        self.end_player_turn()
                        pass  # player.pass

        return False

    def end_player_turn(self):
        self.turn = 'monster'

    def end_monster_turn(self):
        self.turn = 'player'

    def run(self):

        self.level.redraw_manager.run()

        if self.turn == 'monster':
            self.turn_tracker.run()
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
