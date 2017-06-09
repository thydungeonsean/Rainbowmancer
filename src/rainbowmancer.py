import pygame
from pygame.locals import *
from map.master_map import MasterMap
from map.terrain_map import TerrainMap

    
pygame.init()
pygame.display.set_mode((800, 600))


def demo():

    screen = pygame.display.get_surface()
    
    map = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 3, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 0, 0, 1, 0, 0, 4, 1, 1],
        [1, 1, 0, 0, 1, 1, 0, 4, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 3, 0, 0, 1],
        [1, 1, 0, 2, 0, 3, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

    m = MasterMap()
    t = TerrainMap(10, 10)
    t.set_map(map)

    m.set_terrain_map(t)
    m.initialize()

    m.color_map.red_map.add_source((4, 4), 5)
    m.color_map.green_map.add_source((8, 6), 4)
    m.color_map.blue_map.add_source((2, 2), 5)
    m.color_map.red_map.add_source((1, 8), 5)
    m.color_map.green_map.add_source((1, 8), 5)
    m.map_image.redraw_all_maps()
    m.map_image.draw(screen, ('a', 0))
    

def main():
    
    demo()
    
    pygame.display.update()
    while pygame.event.wait().type != KEYDOWN:
        pass

