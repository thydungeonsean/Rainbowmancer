import pygame
from pygame.locals import *

from src.map.mapgen.level_gen import LevelGen

from turn_tracker import TurnTracker
from effect_tracker import EffectTracker
from src.state.ui.ui import UI
from game_display import GameDisplay
from pointer import Pointer
from highlighter import Highlighter


class Game(object):

    FPS = 60

    zoom_screen_w = 9
    zoom_screen_h = 7

    def __init__(self, player_key):

        self.level = None
        self.player = None
        self.player_key = player_key
        self.objects = []

        self.ui = UI(self)

        self.turn_tracker = TurnTracker(self)
        self.turn = 'player'
        self.active_ability = None

        self.effect_tracker = EffectTracker(self)

        self.clock = pygame.time.Clock()
        self.tick = 0

        self.pointer = Pointer(self)
        self.highlighter = Highlighter(self)

        self.sub_screen = pygame.Surface((720, 720)).convert()

        self.game_display = GameDisplay(self)
        self.screen_mode = 'zoomed'

        self.zoomed_sub_screen = pygame.Surface((19 * 16, 15 * 24)).convert()
        self.zoomed_sub_screen_scale = pygame.Surface((19 * 16 * 2, 15 * 24 * 2)).convert()
        self.zoomed_sub_screen_scale_rect = self.zoomed_sub_screen_scale.get_rect()
        self.zoomed_sub_screen_scale_rect.topleft = (56, 0)

    def load_level(self):

        self.level = LevelGen.generate_level(self)

        self.player = self.level.map_object_generator.add_player(self.player_key, self.level.player_start)
        self.level.load_player(self.player)

        # bind ui panels to player
        self.ui.panels['crystal'].load_player()
        self.ui.panels['character'].load_player()
        self.ui.panels['ability'].load_player()

    def increment_tick(self):
        self.tick += 1
        if self.tick > 60:
            self.tick = 0

    def draw(self):

        self.level.map_image.draw(self.sub_screen, self.tick)

        for obj in self.objects:
            obj.draw(self.sub_screen, self.tick)

        for effect in self.effect_tracker.effects:
            effect.draw(self.sub_screen, self.tick)

        self.highlighter.draw(self.sub_screen)

        if self.game_display.screen_mode == 'full':
            self.draw_full()
        elif self.game_display.screen_mode == 'zoomed':
            self.draw_zoomed()

        self.ui.draw(pygame.display.get_surface(), self.tick)

    def draw_full(self):
        screen = pygame.display.get_surface()
        screen.blit(self.sub_screen, self.sub_screen.get_rect())

    def draw_zoomed(self):
        screen = pygame.display.get_surface()
        sw = self.zoomed_sub_screen_scale.get_width()
        sh = self.zoomed_sub_screen_scale.get_height()

        sub_screen_offset = self.get_screen_coord()
        rect = self.sub_screen.get_rect()
        rect.topleft = sub_screen_offset

        self.zoomed_sub_screen.fill((0, 0, 0))
        self.zoomed_sub_screen.blit(self.sub_screen, rect)

        pygame.transform.scale(self.zoomed_sub_screen, (sw, sh), self.zoomed_sub_screen_scale)
        screen.blit(self.zoomed_sub_screen_scale, self.zoomed_sub_screen_scale_rect)

    def get_screen_coord(self):
        x, y = self.player.coord

        sx = x - Game.zoom_screen_w
        sy = y - Game.zoom_screen_h

        return sx * -16, sy * -24

    def switch_screen_mode(self):
        self.game_display.switch_screen_mode()

    def handle_input(self):

        # returns true to exit game

        for event in pygame.event.get():

            if event.type == QUIT:
                return True

            elif event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    return True

                elif event.key == K_SLASH:
                    self.switch_screen_mode()

                if self.turn == 'player' and self.effect_tracker.effects_clear():
                    if self.active_ability is not None and event.key in self.active_ability.valid_keys:

                        self.active_ability.handle_player_input(self.pointer, event)

                    else:
                        self.handle_player_input(event)

            elif event.type == MOUSEBUTTONDOWN:

                if event.button == 1:  # left click
                    if not self.ui.click(pygame.mouse.get_pos()):  # no icon clicked
                        pass  # handle clicking the screen

                elif event.button == 3:  # right click
                    if not self.ui.right_click(pygame.mouse.get_pos()):
                        pass  # handle right clicking the screen

            elif event.type == MOUSEMOTION:

                self.pointer.mouse_moved()

        return False

    def handle_player_input(self, event):
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

    def end_player_turn(self):
        self.turn = 'monster'

    def end_monster_turn(self):
        self.turn = 'player'

    def run(self):

        self.level.redraw_manager.run()

        if self.turn == 'monster' and self.effect_tracker.effects_clear():
            self.turn_tracker.run()
        # run effects

        self.effect_tracker.run()

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

    def set_active_ability(self, ability):
        self.active_ability = ability

    def clear_active_ability(self):
        self.active_ability = None
