from __future__ import division
from random import randint, uniform
from math import sin, cos, degrees, radians, pi, atan2
from itertools import chain
import pygame as pg
from .. import prepare


def point_vector(p1, p2):
    x = p2[0] - p1[0]
    y = p2[1] - p1[1]
    try:
        x = x / abs(x)
    except ZeroDivisionError:
        pass
    try:
        y = y / abs(y)
    except ZeroDivisionError:  
        pass
    return (x, y)
    

        
class Cow(object):
    name = "cow"
    def __init__(self, center_point, angle):
        self.image = prepare.GFX["blockycow"]
        self.rot_image = self.image
        self.pos = center_point
        self.rect = self.image.get_rect(center=center_point)
        self.angle = pi * angle
        self.speed = .3
        self.max_speed = 1.2
        self.turn_speed = .01
        self.boost = 0
        self.max_boost = 1
        self.health = 100.0
        self.belly = 100.0
        self.lassoed = False
        self.rescued = False
        
    def move_turn(self, multiplier=1):    
        if self.angle < 0:
            self.angle = (pi * 2) - (-1 * self.angle)
        if self.angle >= pi * 2:
            self.angle = self.angle - (pi * 2)
        speed = self.speed + self.boost
        vx = speed * cos(self.angle) * multiplier
        vy = speed * sin(self.angle) * multiplier
        self.pos = (self.pos[0] + vx, self.pos[1] - vy)
        self.rect.center = self.pos
    
    def move(self, offset):
        self.pos = (self.pos[0] + offset[0], self.pos[1] + offset[1])
        self.rect.center = self.pos
        
    def get_neighbors(self, cows):
        collision_rect = self.rect.inflate(40, 40)
        return [c for c in cows if c.rect.colliderect(collision_rect) and c != self]
        
    def seek_angle(self, angle):
        if atan2(sin(angle - self.angle), cos(angle - self.angle)) < 0:
            return -self.turn_speed
        else:
            return self.turn_speed
            
    def update_image(self):
        self.rot_image = pg.transform.rotate(self.image, degrees(self.angle) - 90)
        self.rect = self.rot_image.get_rect(center=self.pos)
        
    def collide_with_object(self, obj):
        if obj.solid:
            if obj.name == "cactus":
                self.health -= 1
            if "fence" in obj.name:
                self.angle += pi
            offset = point_vector(self.pos, obj.pos)
            self.pos = (self.pos[0] + -offset[0], self.pos[1] + -offset[1])
            self.rect.center = self.pos
        else:    
            if "grass" in obj.name:
                self.belly += 1
            elif "airstrip" in obj.name:
                self.rescued = True
                
                
    def update(self, cows_list, obstacles_list):
        cows = cows_list
        obstacles = obstacles_list
        self.belly -= .005
        self.boost -= .007
        if self.boost < 0:
            self.boost = 0
        
        c_rect = pg.Rect(0, 0, 16, 16)
        c_rect.center = self.pos
        collisions = [x for x in obstacles if x.rect.colliderect(c_rect)]
        for c in collisions:
            if c.name == "cactus":
                if c.collision_rect.colliderect(self.rect):
                    self.collide_with_object(c)
            else:
                self.collide_with_object(c)
   
        if not self.lassoed:
            total = 0
            allx, ally = 0, 0
            count = 0
            neighbors = self.get_neighbors(cows)
            for cow in neighbors:
                total += self.seek_angle(cow.angle) * .2
                rect1 = pg.Rect(0, 0, 16, 16)
                rect1.center = self.pos
                rect2 = pg.Rect(0, 0, 16, 16)
                rect2.center = cow.pos
                if rect1.colliderect(rect2):
                    count += 1
                    x, y = point_vector(rect1.center, rect2.center)
                    allx += x
                    ally += y
            if count:
                allx, ally = allx / count, ally / count        
            else:
                allx, ally = 0, 0
            self.pos = (self.pos[0] + (-allx), self.pos[1] + (-ally))
            if neighbors:
                self.angle += (total / len(neighbors)) * .5
        
                    
    def draw_icon(self, surface, offset):
        icon = pg.Rect(0, 0, 4, 4)
        icon.center = ((self.rect.centerx + offset[0])/ 5, (self.rect.centery + offset[1]) / 5)
        pg.draw.rect(surface, pg.Color("white"), icon)
                            
    def draw(self, surface):
        self.update_image()
        surface.blit(self.rot_image, self.rect)
                