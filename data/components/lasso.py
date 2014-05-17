from math import cos, sin, pi, atan2
from itertools import chain
import pygame as pg


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

    
class Lasso(object):
    def __init__(self, cowboy):
        self.done = False
        self.cowboy = cowboy
        self.angle = self.cowboy.angle 
        self.radius = 6
        self.max_radius = 30
        self.ticks = 0
        self.flight_time = 0
        self.flight_start = 0
        self.anchor = self.cowboy.pos
        self.center = self.cowboy.pos
        self.length = 1.0
        self.max_length = 60.0
        self.state = "Windup"
        
    def get_event(self, event):
        if self.state == "Windup":
            self.throw()
        elif self.state == "Attached":
            self.done = True
            self.target.lassoed = False
            
    def throw(self, power=1):
        self.angle = self.cowboy.angle
        self.update_loop_coords()
        self.state = "Aloft"
        self.flight_start = self.ticks
        self.flight_time = (self.length / self.max_length) * 180
        
    def update_loop_coords(self):
        loop_length = self.length - self.radius
        self.center = (int(self.anchor[0] + (cos(self.angle) * self.length)),
                             int(self.anchor[1] - (sin(self.angle) * self.length)))
        self.loop_anchor = (int(self.anchor[0] + (cos(self.angle) * loop_length)),
                                     int(self.anchor[1] - (sin(self.angle) * loop_length)))
        self.rect = pg.Rect(0, 0, self.radius * 2, self.radius * 2)
        self.rect.center = self.center

        
    def fly(self):
        self.length += 1.5
        self.update_loop_coords()
               
    def get_angle(self, pos):
        x_dist = pos[0] - self.anchor[0]
        y_dist = pos[1] - self.anchor[1] 
        return atan2(-y_dist, x_dist)
        
    def update(self, cows, wolves):
        self.ticks += 1
        self.anchor = self.cowboy.pos
        if self.state == "Windup":
            self.radius += .04
            self.radius = min(self.radius, self.max_radius)
            self.angle += .1
            self.angle = self.angle % (pi * 2)             
            self.length += .1
            self.length = min(self.length, self.max_length)
            self.update_loop_coords()
        
        elif self.state == "Aloft":
            if self.ticks - self.flight_start > self.flight_time:
                self.done = True
                              
            else:
                self.fly()
                for animal in chain(cows, wolves):
                    if pg.sprite.collide_circle(self, animal):
                        self.state = "Attached"
                        self.target = animal
                        self.target.lassoed = True
                        self.target.angle = self.angle + pi
                        break
                       
                        
        elif self.state == "Attached":
            vec = point_vector(self.target.pos, self.anchor)
            self.target.angle = self.get_angle(self.target.pos) + pi
            self.target.move_turn(multiplier=2)
            
        
            
                
            
    def draw(self, surface):
        if self.state in ("Windup", "Aloft"):
            center = (int(self.center[0]), int(self.center[1]))
            pg.draw.circle(surface, pg.Color("white"), center, int(self.radius), 1)
            pg.draw.line(surface, pg.Color("white"), self.anchor, self.loop_anchor)
        elif self.state == "Attached":
            pg.draw.line(surface, pg.Color("white"), self.anchor, self.target.pos)
        