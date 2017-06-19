import pygame
from src.state.game import Game


pygame.init()
pygame.display.set_mode((800, 600))


def main():

    p = 'player'

    g = Game(p)
    g.load_level()

    g.main()

