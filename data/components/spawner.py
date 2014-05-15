from random import randrange
import pygame as pg
from .wolf import Wolf

class WolfSpawner(object):
    def __init__(self, center_point):
        self.pos = center_point
        self.check_rect = pg.Rect(0, 0, 800, 800)    
        self.check_rect.center = self.pos
        
    def update(self, wolves):
        if randrange(10000) < 2:
            num_wolves = len([x for x in wolves if self.check_rect.collidepoint(x.pos)])
            if num_wolves < 2:
                wolves.append(Wolf(self.pos))
            
    def move(self, offset):
        self.pos = (self.pos[0] + offset[0], self.pos[1] + offset[1])
        self.check_rect.center = self.pos