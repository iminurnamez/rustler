import pygame as pg
from .. import tools, prepare
from ..components.labels import TransparentGroupLabel as TGLabel
from ..components.labels import TransparentLabel as TLabel
class ControlsScreen(tools._State):
    def __init__(self):
        super(ControlsScreen, self).__init__()
        self.next = "GAME"
        self.fps = 60
        screen_rect = pg.display.get_surface().get_rect()
        self.labels = []
        title = TGLabel(self.labels, 64, "CONTROLS", "gray1", "midtop",
                               screen_rect.centerx, 30)
        top = title.rect.bottom + 40
        left = 310
        second_left = 610
        lines = [("Horse Speed", "UP, DOWN"), ("Turn Horse", "LEFT, RIGHT"),
                    ("Crack Whip", "W"), ("Fire Pistol", "SPACE"), ("Equip Lasso", "S"),
                    ("Throw Lasso", "S"), ("Detach Lasso", "S"), ("Toggle Map", "M"),
                    ("Toggle Fullscreen", "F"), ("Exit", "ESCAPE")] 
        for line in lines:
            label = TGLabel(self.labels, 36, line[0], "gray1", "topleft", left, top)
            label2 = TGLabel(self.labels, 36, line[1], "gray1", "topleft", second_left, top)
            top += label.rect.height + 20
        self.start = TLabel(48, "Press SPACE to start", "gray1", "midbottom",
                                   screen_rect.centerx, screen_rect.bottom - 30)
        self.ticks = 0
        self.show_start = False
        
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.done = True
                
    def update(self, surface, keys):
        self.ticks += 1
        if not self.ticks % 40:
            self.show_start = not self.show_start
        self.draw(surface)
        
    def draw(self, surface):
        surface.fill(pg.Color("tan"))
        for label in self.labels:
            label.draw(surface)
        if self.show_start:
            self.start.draw(surface)
                                            