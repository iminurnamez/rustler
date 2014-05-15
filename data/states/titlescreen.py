from random import randint
import pygame as pg
from .. import prepare, tools
from ..components import cows, obstacles
from ..components.labels import TransparentLabel as TLabel


class TitleScreen(tools._State):
    def __init__(self):
        super(TitleScreen, self).__init__()
        self.next = "STORY"
        screen_rect = pg.display.get_surface().get_rect()
        self.title = TLabel(192, "R.U.S.T.L.E.R.", "gray1", "midtop",
                                   screen_rect.centerx, 50)
        self.instruct = TLabel(64, "Press SPACE to play", "gray1", "midbottom",
                                        screen_rect.centerx, screen_rect.bottom - 50)                                   
        
        self.obstacles = [obstacles.BigRock((100, 100), None),
                                 obstacles.SmallRock((400, 300), None),
                                 obstacles.SmallRock((600, 600), None)]

        for _ in range(15):
            _point = (randint(50, screen_rect.width - 50),
                         randint(50, screen_rect.height - 50))
            self.obstacles.append(obstacles.Grass(_point, None))
        self.cows = []
        for i in range(10):
            point = (randint(100, screen_rect.width - 100),
                         randint(100, screen_rect.height - 100))
            self.cows.append(cows.Cow(point))
        
        
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.done = True
                
    def update(self, surface, keys):
        for cow in self.cows:
            cow.update(self.cows, self.obstacles)
            cow.move_turn()
        self.draw(surface)

    def draw(self, surface):
        surface.fill(pg.Color("tan"))
        for obst in self.obstacles:
            obst.draw(surface)
        for cow in self.cows:
            cow.draw(surface)
        self.title.display(surface)
        self.instruct.display(surface)
        