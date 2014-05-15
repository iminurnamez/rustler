import pygame as pg
from .. import prepare


class Tile(object):
    def __init__(self, lefttop, image_name):
        self.name = image_name
        self.image = prepare.GFX[image_name]
        self.rect = self.image.get_rect(topleft=lefttop)
        self.pos = self.rect.center
        self.dirty = True
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
    def move(self, offset):
        self.rect.move_ip(offset)
        
class Desert(Tile):
    terrain = "desert"
    def __init__(self, lefttop, orientation):
        super(Desert, self).__init__(lefttop, "desert")
        
class Grass(Tile):
    terrain = "grass"
    def __init__(self, lefttop, orientation):
        super(Grass, self).__init__(lefttop, "grass")
        
class Cliff(Tile):
    terrain = "cliff"
    def __init__(self, lefttop, orientation):
        super(Cliff, self).__init__(lefttop, "cliff" + orientation)

        
class Rock(Tile):
    terrain = "rock"
    def __init__(self, lefttop, orientation):
        super(Rock, self).__init__(lefttop, "rock" + orientation)
              
        
        
        
        
        
        
        
