import pygame
from src.state.game import Game
import os
from pygame.locals import *


def init():
    pygame.init()

    # set basic resolution to 1280 x 720 - width is cheaper than height for our purpose
    # 4:3 960 x 720
    # 16:9 1280 x 720
    pygame.display.set_mode((960, 720))
    os.environ['SDL_VIDEO_CENTERED'] = "TRUE"


def main():

    init()

    p = 'player'

    g = Game(p)
    g.load_level()

    g.main()


