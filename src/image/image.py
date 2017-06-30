import pygame


class Image(object):

    TILEW = 16
    TILEH = 24

    @classmethod
    def load(cls, t_id):
        c = cls()
        c.surf = pygame.image.load(''.join(('assets/', t_id, '.png')))
        c.rect = c.surf.get_rect()
        return c
        
    @classmethod
    def blank(cls, w, h):
        c = cls()
        c.surf = pygame.Surface((w, h))
        c.surf.fill((0, 0, 0))
        c.rect = c.surf.get_rect()
        return c
        
    @classmethod
    def filled(cls, fill=(255, 255, 255)):
        c = cls()
        c.surf = pygame.Surface((cls.TILEW, cls.TILEH))
        c.surf.fill(fill)
        c.rect = c.surf.get_rect()
        return c
        
    def __init__(self):
    
        self.surf = None
        self.rect = None
        self.color = (255, 255, 255)
    
    def position(self, (x, y)):
        self.rect.topleft = x * Image.TILEW, y * Image.TILEH

    def position_pixel(self, (x, y)):
        self.rect.topleft = x, y
    
    def draw(self, surface):
        surface.blit(self.surf, self.rect)
        
    def recolor(self, color):
        p = pygame.PixelArray(self.surf)
        p.replace(self.color, color)
        self.color = color