import pygame as pg
from .. import prepare
from ..components import bullet
from random import randint, uniform
from math import sin, cos, degrees, radians, pi, atan2
from itertools import chain


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

class Cowboy(object):
    def __init__(self, center_point):
        self.name = "cowboy"
        self.image = prepare.GFX["cowboy"]
        self.rot_image = self.image
        self.pos = center_point
        self.rect = self.image.get_rect(center=center_point)
        self.angle = radians(90)
        self.turn_speed = .02
        self.speed = .1
        self.max_speed = 1.25
        self.bullets = 200
        self.health = 100
        self.gun_sound = prepare.SFX["gun_sound"]

                   
    def shoot(self, bullets):
        if self.bullets > 0:
            self.gun_sound.play()
            self.rot_image = pg.transform.laplacian(self.rot_image)

            bullets.append(bullet.Bullet(self.pos, self.angle))
            self.bullets -= 1
        
    def get_angle(self, cow):
        x_dist = cow.pos[0] - self.pos[0]
        y_dist = cow.pos[1] - self.pos[1] 
        return atan2(-y_dist,x_dist)
        
    def get_neighbors(self, cows):
        collision_rect = self.rect.inflate(120, 120)
        return [c for c in cows if c.rect.colliderect(collision_rect)]
            
    def accelerate(self, num):
        self.speed += .01 * num
        self.speed = min(max(0, self.speed), self.max_speed)
                   
    def update(self, cows, obstacles):
        if self.angle < 0:
            self.angle = (pi * 2) - (-1 * self.angle)
        if self.angle >= pi * 2:
            self.angle = self.angle - (pi * 2)
        vx = self.speed * cos(self.angle)
        vy = self.speed * sin(self.angle)
        self.pos = (self.pos[0] + vx, self.pos[1] - vy)
        self.rect.center = self.pos
        for cow in self.get_neighbors(cows):
            if not cow.lassoed:
                new_angle = self.get_angle(cow)
                cow.angle += cow.seek_angle(new_angle)   
        c_rect = pg.Rect(self.pos, (10, 10))
        for obst in obstacles:
            if obst.rect.colliderect(c_rect):
                if obst.name == "cactus":
                    if c_rect.colliderect(obst.collision_rect):
                        self.collide_with_object(obst)
                else:
                    self.collide_with_object(obst)
                
                
    def collide_with_object(self, obj):
        if obj.solid:
            if obj.name == "cactus":
                self.health -= 1
            
            offset = point_vector(self.pos, obj.pos)
            self.pos = (self.pos[0] + -offset[0], self.pos[1] + -offset[1])
            self.rect.center = self.pos
        
                  
    def move_turn(self):    
        vx = self.speed * cos(self.angle)
        vy = self.speed * sin(self.angle)
        self.pos = (self.pos[0] + vx, self.pos[1] - vy)
        self.rect.center = self.pos
    
    def move(self, offset):
        self.pos = (self.pos[0] + offset[0], self.pos[1] + offset[1])
        self.rect.center = self.pos
        
    def update_image(self):
        self.rot_image = pg.transform.rotate(self.image, degrees(self.angle))
        self.rect = self.rot_image.get_rect(center=self.pos)
    
    def draw_icon(self, surface, offset):
        icon = pg.Rect(0, 0, 4, 4)
        icon.center = ((self.rect.centerx + offset[0])/ 5, (self.rect.centery + offset[1]) / 5)
        pg.draw.rect(surface, pg.Color("blue"), icon)
        
    def draw(self, surface):
        self.update_image()
        
        surface.blit(self.rot_image, self.rect)