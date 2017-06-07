import pygame
from pygame.locals import *
from random import randint
from color.color import Color
from src.image.tileset import TileSet
from src.image.image import Image
from src.color.color_palette import *
from src.map.color_map import ColorMap
from src.map._map import _Map


def rand_color():
    
    r = randint(1, 255)
    #g = randint(1, 255)
    b = randint(1, 255)
    #return (r, g, b)
    return (r, 0, b)
    
pygame.init()
screen = pygame.display.set_mode((800, 600))

tileset = TileSet('enviro', 'main')

tiles = {
'v_wall': Image.load('v_wall'),
'h_wall': Image.load('h_wall'),
'grass': Image.load('grass'),
'floor': Image.blank()
}

def demo():

    global tiles, screen, tileset
    
    map = [
    [2, 1, 1, 1, 1, 1, 1, 2, 1, 2],
    [2, 0, 0, 0, 0, 0, 0, 2, 3, 2],
    [2, 0, 1, 1, 2, 0, 1, 1, 0, 2],
    [2, 0, 0, 0, 2, 0, 0, 0, 0, 2],
    [2, 2, 0, 0, 2, 0, 0, 2, 2, 2],
    [2, 2, 0, 0, 2, 2, 0, 2, 2, 2],
    [2, 1, 1, 1, 1, 1, 0, 1, 1, 2],
    [2, 0, 0, 0, 0, 0, 3, 0, 0, 2],
    [2, 2, 0, 3, 0, 3, 0, 0, 0, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    ]
    
    map_tiles = {
    0: tiles['floor'],
    1: tiles['h_wall'],
    2: tiles['v_wall'],
    3: tiles['grass']
    }
    
    w = 16
    h = 24
    
    c = Color(RED_1)
    bc = Color(0, 255, 255)
    #c.add(bc)
    
    for y in range(10):
        for x in range(10):
            t = map_tiles[map[y][x]]
            t.position((x*w, y*h))
            t.recolor(c.get())
            t.draw(screen)
            
    tileset.get_tile_image('tuft_2').draw(screen)
    
    ton = _Map(10, 10)
    c = ColorMap(ton, 'red')
    c.add_source((0, 0), 5)
    c.add_source((2, 2), 3)
    c.print_map()


def main():
    
    demo()
    
    pygame.display.update()
    while pygame.event.wait().type != KEYDOWN:
        pass
   
main()