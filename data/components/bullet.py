from math import sin, cos
import pygame as pg


class Bullet(object):
    def __init__(self, center_point, angle):
        self.pos = center_point
        self.rect = pg.Rect(0, 0, 2, 2)
        self.rect.center = self.pos
        self.angle = angle
        self.speed = 4
        self.ticks = 0
        self.done = False
        
    def move_turn(self):    
        vx = self.speed * cos(self.angle)
        vy = self.speed * sin(self.angle)
        self.pos = (self.pos[0] + vx, self.pos[1] - vy)
        self.rect.center = self.pos
        
    def move(self, offset):
        self.pos = (self.pos[0] + offset[0], self.pos[1] + offset[1])
        self.rect.center = self.pos
        
    def update(self, wolves, cows, obstacles):
        self.ticks += 1
        if self.ticks > 300:
            self.done = True
        self.move_turn()
        wolf_hits = [x for x in wolves if x.rect.collidepoint(self.pos)]
        if wolf_hits:
            wolf_hits[0].health -= 100
            self.done = True
        else:
            for cow in cows:
                if cow.rect.collidepoint(self.pos):
                    cow.health -= 100
                    self.done = True
                    break
            if not self.done:
                for obst in [x for x in obstacles if x.rect.collidepoint(self.pos)]:
                    if obst.solid:
                        self.done = True
                        break

    def draw(self, surface):
        b_rect = pg.Rect(0, 0, 2, 2)
        b_rect.center = self.pos
        pg.draw.rect(surface, pg.Color("gray10"), b_rect)
                
    