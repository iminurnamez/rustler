import pygame as pg
from .. import tools, prepare


class WorldMap(tools._State):
    def __init__(self):
        super(WorldMap, self).__init__()
        self.next = "GAME"
        
    def startup(self, persistent):
        self.image = persistent["worldmap"]
        self.start_time = pg.time.get_ticks()
    
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_m:
                self.done = True
                self.persist["pause time"] = pg.time.get_ticks() - self.start_time
                
    def update(self, surface, keys):
        self.draw(surface)        
        
    def draw(self, surface):
        surface.blit(self.image, (0, 0))
                                              
         