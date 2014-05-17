from math import degrees
import pygame as pg
from .. import prepare


class Obstacle(object):
    def __init__(self, center_point, image_name):
        self.name = image_name
        self.image = prepare.GFX[image_name]
        self.rect = self.image.get_rect(center=center_point)
        self.pos = center_point
        self.solid = True
        
    def move(self, offset):
        self.pos = (self.pos[0] + offset[0], self.pos[1] + offset[1])
        self.rect.center = self.pos
        
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
    def draw_icon(self, surface, offset):
        pass
        

class Cactus(Obstacle):
    def __init__(self, center_point, orientation):
        super(Cactus, self).__init__(center_point, "cactus")
        self.collision_rect = pg.Rect(0, 0, 20, 20)
        self.collision_rect.midbottom = self.rect.midbottom
        self.icon_img = prepare.GFX["tinycactus"]
        
    def move(self, offset):
        self.pos = (self.pos[0] + offset[0], self.pos[1] + offset[1])
        self.rect.center = self.pos
        self.collision_rect.midbottom = self.rect.midbottom
        
    def draw_icon(self, surface, offset):
        icon = pg.Rect(0, 0, 5, 10)
        icon.center = ((self.rect.centerx + offset[0])/ 5, (self.rect.centery + offset[1]) / 5)
        surface.blit(self.icon_img, icon)
        

class Fence(Obstacle):
    def __init__(self, center_point, orientation):
        super(Fence, self).__init__(center_point, "fence" + orientation)
        
class Grass(Obstacle):
    def __init__(self, center_point, orientation):
        super(Grass, self).__init__(center_point, "grass")
        self.solid = False
        
    def draw_icon(self, surface, offset):
        icon = pg.Rect(0, 0, 2, 2)
        icon.center = ((self.rect.centerx + offset[0])/ 5, (self.rect.centery + offset[1]) / 5)
        pg.draw.rect(surface, pg.Color("darkgreen"), icon)
        
class SmallRock(Obstacle):
    def __init__(self, center_point, orientation):
        super(SmallRock, self).__init__(center_point, "smallrock")
        self.icon_img = prepare.GFX["tinysmallrock"]
        
    def draw_icon(self, surface, offset):
        icon = pg.Rect(0, 0, 4, 4)
        icon.center = ((self.rect.centerx + offset[0])/ 5, (self.rect.centery + offset[1]) / 5)
        surface.blit(self.icon_img, icon)
        
class BigRock(Obstacle):
    def __init__(self, center_point, orientation):
        super(BigRock, self).__init__(center_point, "bigrock")
        self.icon_img = prepare.GFX["tinybigrock"]
        
    def draw_icon(self, surface, offset):
        icon = pg.Rect(0, 0, 8, 8)
        icon.center = ((self.rect.centerx + offset[0])/ 5, (self.rect.centery + offset[1]) / 5)
        surface.blit(self.icon_img, icon)
    
class Airstrip(Obstacle):
    def __init__(self, center_point, orientation):
        super(Airstrip, self).__init__(center_point, "airstrip")
        self.solid = False
    
    def draw_icon(self, surface, offset):
        icon = pg.Rect(0, 0, 60, 20)
        icon.center = ((self.rect.centerx + offset[0])/ 5, (self.rect.centery + offset[1]) / 5)
        pg.draw.rect(surface, pg.Color("saddlebrown"), icon)
        
class Carcass(object):
    def __init__(self, angle, pos):
        self.name = "cowskeleton"
        img = prepare.GFX["cowskeleton"]
        self.image = pg.transform.rotate(img, degrees(angle) - 90)
        self.pos = pos
        self.rect = self.image.get_rect(center=self.pos)
        self.solid = False
        
    def move(self, offset):
        self.pos = (self.pos[0] + offset[0], self.pos[1] + offset[1])
        self.rect.center = self.pos
           
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
    def draw_icon(self, surface, offset):
        pass
