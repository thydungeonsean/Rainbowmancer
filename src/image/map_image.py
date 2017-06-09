import pygame
from tileset import TileSet


class MapImage(object):

    TILEW = 16
    TILEH = 24

    def __init__(self, m_map):
        
        self.map = m_map
        
        self.tileset = TileSet.get_enviro_tiles()
        
        self.needs_redraw = True
        
        self.images = {
            ('a', 0): None,
            ('b', 0): None,
            ('a', 1): None,
            ('b', 1): None
        }
        
        self.rect = None
        
        self.init_map_images()
        
    def set_redraw(self):
        self.needs_redraw = True
        # redraw if:
        #     light sources changes
        #     player moves (fov changes)
        #     tile changes
        
    def init_map_images(self):
        
        mw = self.map.w * MapImage.TILEW
        mh = self.map.h * MapImage.TILEH
        
        self.images[('a', 0)] = pygame.Surface((mw, mh)).convert()
        self.images[('b', 0)] = pygame.Surface((mw, mh)).convert()
        self.images[('a', 1)] = pygame.Surface((mw, mh)).convert()
        self.images[('b', 1)] = pygame.Surface((mw, mh)).convert()
        
        self.rect = self.images[('a', 0)].get_rect()

        self.redraw_all_maps()

    def redraw_all_maps(self):

        self.render_map(('a', 0))
        self.render_b_map(0)
        
        self.render_map(('a', 1))
        self.render_b_map(1)
    
    def draw_tile_batch(self, surface, points, (ani, col_mod)):
        
        for point in points:
            self.draw_tile(surface, point, (ani, col_mod))
    
    def draw_tile(self, surface, (px, py), (ani, col_mod)):
        
        tl_map = self.map.tile_map
        cls = MapImage
        
        tile_key = tl_map.get_tile_key((px, py))
        if tl_map.point_is_animated((px, py)):
            tile_key = '_'.join((tile_key, ani))
            
        color = self.map.color_map.get_tile_color(col_mod, (px, py))
        
        tile = self.tileset.get_tile_image(tile_key)
        tile.recolor(color)
        tile.position((px*cls.TILEW, py*cls.TILEH))
        
        tile.draw(surface)
        
    def render_map(self, map_id):
    
        points = self.map.terrain_map.all_points
        self.draw_tile_batch(self.images[map_id], points, map_id)
        
    def render_b_map(self, col_mod):
    
        img = self.images[('b', col_mod)]
        img.blit(self.images[('a', col_mod)], img.get_rect())  # copy a_map onto surface
        
        # get ani tiles and only update those
        points = list(filter(self.map.tile_map.point_is_animated, self.map.tile_map.all_points))
     
        self.draw_tile_batch(img, points, ('b', col_mod))
    
    def draw(self, surface, map_id):

        # or get map_id from other context

        surface.blit(self.images[map_id], self.rect)
        
    
    
    