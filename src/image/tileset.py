from src.image.tilesheet_key_parser import *
from src.image.image import Image
import pygame


class TileSet(object):

    enviro = None
    border = {
        'main': None,
        'ornate': None
    }

    ui = None
    icons = None

    @classmethod
    def get_enviro_tiles(cls):
        if cls.enviro is None:
            cls.enviro = cls('enviro', 'main')
        return cls.enviro

    @classmethod
    def get_border_tiles(cls, style='main'):
        if cls.border[style] is None:
            cls.border[style] = cls('border', 'main')
        return cls.border[style]

    @classmethod
    def get_ui_tiles(cls):
        if cls.ui is None:
            cls.ui = cls('ui', 'ui')
        return cls.ui

    @classmethod
    def get_icon_tiles(cls):
        if cls.icons is None:
            cls.icons = cls('ui', 'ui', sheet='icons')
        return cls.icons

    def __init__(self, set_type, set_id, sheet='assets'):

        self.sheet = sheet
        self.sheet_key = ''.join((self.sheet, '_key'))
        self.tilesheet = self.load_tilesheet()
        
        self.tile_w, self.tile_h = self.load_tile_dimensions()
        # self.colorkey = self.load_colorkey()
        
        self.tileset_pos_dict = self.set_tileset_dictionary(set_type, set_id)
        self.tiles = self.load_tiles()
       
    def load_tilesheet(self):
        return pygame.image.load(''.join((os.path.dirname(__file__), '\\..\\..\\assets\\', self.sheet, '.png')))
       
    def load_tile_dimensions(self):
        return get_tile_dimensions(self.sheet_key)
        
    def load_colorkey(self):
        return get_colorkey(self.sheet_key)
        
    def set_tileset_dictionary(self, set_type, set_id):
        
        type_key = ''.join((set_type, ' sets'))
        type_block = parse_block(get_block(self.sheet_key, type_key), 'set')
        set_line = get_key_line(type_block, set_id)
        
        set_type_offset = (set_line[2], set_line[1])
        
        tile_list_key = ''.join((set_type, ' set tiles'))
        tile_list_block = parse_block(get_block(self.sheet_key, tile_list_key), 'tile')
        
        tileset_dict = self.create_tileset_dict(tile_list_block, set_type_offset)
        return tileset_dict

    def create_tileset_dict(self, tile_list_block, (set_x, set_y)):
        tileset_dict = {}
        for key, x, y in tile_list_block:
            tileset_dict[key] = (x+set_x, y+set_y)
        return tileset_dict  
        
    def load_tiles(self):
        tiles = {}
        for key in self.tileset_pos_dict.keys():
            tile_image = self.set_tile_image(key)
            tiles[key] = tile_image
        return tiles
            
    def set_tile_image(self, key):
        tile = Image.blank(self.tile_w, self.tile_h)
        tx, ty = self.tileset_pos_dict[key]
        tile.surf.blit(self.tilesheet, (0, 0), (tx*self.tile_w, ty*self.tile_h, self.tile_w, self.tile_h))
        # tile.auto_scale()
        return tile
        
    def get_tile_image(self, tile_key):
        return self.tiles[tile_key]

    def get_any_tile_id(self):
        return self.tiles.keys()[0]
