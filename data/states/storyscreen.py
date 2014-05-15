import pygame as pg
from .. import tools, prepare
from ..components.labels import TransparentLabel as TLabel
from ..components.labels import TransparentGroupLabel as TGLabel



class StoryScreen(tools._State):
    def __init__(self):
        super(StoryScreen, self).__init__()
        self.next = "GAME"
        lines = ["Disenchanted with the constant barrage of ineffectual",
                    "e-mails from MooveOn.org and disgusted by the",
                    "seeming success of the National Boltgun Association's",
                    "new \"Boltguns don't kill cows, humans do\" campaign,",
                    "you have joined a more militant group dedicated to",
                    "direct action: R.U.S.T.L.E.R. (Rescuing Ungulates So",
                    "They Live in Excellent Resplendence). You'll be on the",
                    "front lines of the fight for bovid rights escorting refugee",
                    "cows to clandestine airstrips so grab your ten-gallon hat,",
                    "load your six-shooter and get those dogies mooving!"]
        
        self.labels = []
        screen_rect = pg.display.get_surface().get_rect()
        centerx = screen_rect.centerx
        top = screen_rect.height + 5
        for line in lines:
            label = TGLabel(self.labels, 48, line, "gray1", "midtop", centerx, top)
            top += label.rect.height + 10
        self.instruct_label = TLabel(64, "Press SPACE to continue", "gray1",
                                                "midbottom", centerx, screen_rect.height - 20)
        self.ticks = 0

    def update(self, surface, keys):
        if self.labels[0].rect.top > 5:
            if not self.ticks % 3:
                for label in self.labels:
                    label.rect.move_ip(0, -1)
        
        self.draw(surface)
        self.ticks += 1
        
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.done = True
            
    def draw(self, surface):
        surface.fill(pg.Color("tan"))
        for label in self.labels:
            label.display(surface)
        if self.labels[0].rect.top <= 5:
            self.instruct_label.display(surface)
            
