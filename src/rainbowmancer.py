import pygame
from pygame.locals import *
from map.master_map import MasterMap
from map.terrain_map import TerrainMap

    
pygame.init()
pygame.display.set_mode((800, 600))


def set_demo():

    screen = pygame.display.get_surface()
    
    map = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 3, 1],
        [1, 0, 1, 2, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 5, 0, 1, 0, 0, 4, 1, 1],
        [1, 1, 0, 0, 1, 1, 0, 4, 1, 1],
        [1, 1, 1, 0, 6, 1, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 3, 0, 0, 1],
        [1, 1, 0, 2, 0, 3, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

    m = MasterMap()
    t = TerrainMap(10, 10)
    t.set_map(map)

    m.set_terrain_map(t)
    m.initialize()

    #m.color_map.add_source(0, (4, 4), 5)
    #m.color_map.add_source(4, (8, 6), 4)
    #m.color_map.add_source('cyan', (2, 2), 5)
    #m.color_map.add_source(6, (1, 8), 5)
    #m.color_map.add_source('blue', (1, 8), 5)
    #m.color_map.add_source('yellow', (8, 1), 1)
    m.color_map.add_source(0, (5, 5), 5)
    m.color_map.add_source(1, (5, 6), 5)
    m.color_map.add_source(2, (4, 5), 5)
    m.map_image.redraw_all_maps()

    return m


def get_m_id(tick):
    if tick < 15:
        return 'a', 0
    elif tick < 30:
        return 'b', 0
    elif tick < 45:
        return 'a', 1
    else:
        return 'b', 1

def draw(m, tick):

    screen = pygame.display.get_surface()

    m_id = get_m_id(tick)

    m.map_image.draw(screen, m_id)


def handle_input():

    for event in pygame.event.get():

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                return True

    return False


def main():
    
    m = set_demo()
    tick = 0

    clock = pygame.time.Clock()

    while True:

        if handle_input():
            break

        clock.tick(60)

        draw(m, tick)
        pygame.display.update()

        tick += 1
        if tick >= 60:
            tick = 0
