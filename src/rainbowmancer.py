import pygame
from pygame.locals import *
from map.master_map import MasterMap
from map.terrain_map import TerrainMap
from src.map.color_source import ColorSource

from map.mapgen import MapGen
from src.state.game import Game
from src.map_objects.player import Player
from src.map_objects.light_component import LightComponent

    
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
    #t = TerrainMap(10, 10)
    t = MapGen.generate_terrain_map_cave(45, 25)

    #t.set_map(map)

    m.set_terrain_map(t)
    m.initialize()

    # m.color_source_generator.get_color_source((2, 10), 'white', 5)
    # m.color_source_generator.get_color_source((20, 16), 'yellow', 5)
    # m.color_source_generator.get_color_source((33, 4), 'blue', 5)
    # m.color_source_generator.get_color_source((15, 10), 'red', 5)
    # m.color_source_generator.get_color_source((30, 13), 'green', 5)
    # m.color_source_generator.get_color_source((25, 16), 'cyan', 5)
    # m.color_source_generator.get_color_source((3, 3), 'purple', 5)

    m.color_map.recompute_maps()

    m.map_image.add_batch_to_redraw(m.terrain_map.all_points)
    m.map_image.redraw_tiles()

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

    p = 'player'

    g = Game(p)
    g.load_level(m)

    m.map_object_generator.create_monster('gnome', (10, 10))


    g.main()

    # while True:
    #
    #     if handle_input():
    #         break
    #
    #     clock.tick(60)
    #
    #     draw(m, tick)
    #     pygame.display.update()
    #
    #     tick += 1
    #     if tick >= 60:
    #         tick = 0
