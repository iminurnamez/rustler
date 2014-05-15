import pygame as pg
from math import sin, cos, degrees, radians, pi, atan2
from random import choice
from .. import prepare


class Wolf(object):
    def __init__(self, center_point):
        self.image = prepare.GFX["wolf"]
        self.rot_image = self.image
        self.pos = center_point
        self.rect = self.image.get_rect(center=center_point)
        self.angle = radians(90)
        self.speed = .4
        self.turn_speed = .02
        self.hunting = False
        self.health = 100
        
        
    def move_turn(self):    
        if self.angle < 0:
            self.angle = (pi * 2) - (-1 * self.angle)
        if self.angle >= pi * 2:
            self.angle = self.angle - (pi * 2)
        speed = self.speed
        vx = speed * cos(self.angle)
        vy = speed * sin(self.angle)
        self.pos = (self.pos[0] + vx, self.pos[1] - vy)
        self.rect.center = self.pos
    
    def move(self, offset):
        self.pos = (self.pos[0] + offset[0], self.pos[1] + offset[1])
        self.rect.center = self.pos
        
    def get_neighbors(self, cows):
        collision_rect = self.rect.inflate(300, 300)
        return [c for c in cows if c.rect.colliderect(collision_rect)]
        
    
            
    def update_image(self):
        self.rot_image = pg.transform.rotate(self.image, degrees(self.angle) - 90)
    
    def collide_with_object(self, obj):
        if "rock" in obj.name or "cactus" in obj.name:
            if obj.name == "cactus":
                self.health -= 1
            
            offset = point_vector(self.pos, obj.pos)
            self.pos = (self.pos[0] + -offset[0], self.pos[1] + -offset[1])
            self.rect.center = self.pos
                    
    def get_angle(self, cow):
        x_dist = cow.pos[0] - self.pos[0]
        y_dist = cow.pos[1] - self.pos[1] 
        return atan2(-y_dist,x_dist)
    
    def seek_angle(self, angle):
        if atan2(sin(angle - self.angle), cos(angle - self.angle)) < 0:
            return -self.turn_speed
        else:
            return self.turn_speed
            
    def update(self, cows, obstacles):
        if not self.hunting:
            neighbors = self.get_neighbors(cows)
            if neighbors:
                self.target = choice(neighbors)
                self.hunting = True
            else:
                self.angle += .001
        else:
            c_rect = pg.Rect(0, 0, 8, 8)
            c_rect.center = self.pos
            if self.target.rect.colliderect(c_rect):
                self.target.health -= 1
                
            else:
                target_angle = self.get_angle(self.target)
                self.angle += self.seek_angle(target_angle)
            if self.target.health <= 0:
                self.hunting = False    
        self.move_turn()        
        
        
                
    def draw_icon(self, surface, offset):
        icon = pg.Rect(0, 0, 3, 3)
        icon.center = ((self.rect.centerx + offset[0])/ 8, (self.rect.centery + offset[0]) / 8)
        pg.draw.rect(surface, pg.Color("red"), icon)
                            
    def draw(self, surface):
        self.update_image()
        surface.blit(self.rot_image, self.rect)    