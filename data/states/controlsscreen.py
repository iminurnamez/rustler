import pygame as pg
from .. import tools, prepare
from ..components.labels import TransparentGroupLabel as TGLabel

class ControlsScreen(tools._State):
    def __init__(self):
        super(ControlsScreen, self).__init__()
        self.next = "GAME"
        screen_rect = pg.display.get_surface().get_rect()
        self.labels = []
        title = TGLabel(self.labels, 64, "CONTROLS", "gray1", "midtop",
                               screen_rect.centerx, 50)
        top = title.rect.bottom + 50
        left = 300
        second_left = 600
        lines = [("Horse Speed", "UP, DOWN"), ("Turn Horse", "LEFT, RIGHT"),
                    ("Crack Whip", "W"), ("Fire Pistol", "SPACE"), ("Equip Lasso", "S"),
                    ("Throw Lasso", "S"), ("Detach Lasso", "S"),
                    ("Toggle Map", "M"), ("Exit", "ESCAPE")] 
        for line in lines:
            label = TGLabel(self.labels, 36, line[0], "gray1", "topleft", left, top)
            label2 = TGLabel(self.labels, 36, line[1], "gray1", "topleft", second_left, top)
            top += label.rect.height + 20
        start = TGLabel(self.labels, 48, "Press SPACE to start", "gray1", "midbottom",
                                screen_rect.centerx, screen_rect.bottom - 50)
                                
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.done = True
                
    def update(self, surface, keys):
        self.draw(surface)
        
    def draw(self, surface):
        surface.fill(pg.Color("tan"))
        for label in self.labels:
            label.draw(surface)
                                            