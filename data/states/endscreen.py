import pygame as pg
from ..import tools, prepare
from ..components.labels import TransparentLabel as TLabel
from ..components.labels import TransparentGroupLabel as TGLabel


class EndScreen(tools._State):
    def __init__(self):
        super(EndScreen, self).__init__()
        
        
    def startup(self, persistent):
        screen_rect = pg.display.get_surface().get_rect()
        face = prepare.GFX["cowface"]
        plane_img = prepare.GFX["sideplane"]
        self.plane = pg.Surface(plane_img.get_size())
        self.plane_rect = self.plane.get_rect(topleft=(-250, 200))
        num_cows = persistent["num cows"]
        rescued = persistent["rescued"]
        ratio = rescued / float(num_cows)
        print ratio
        
        cowspots = [(312, 233), (212, 233), (362, 233), (162, 233), (262, 233)]
        for cs in cowspots:
            pg.draw.rect(self.plane, pg.Color("darkgray"), (cs[0] - 2, cs[1] - 2, 25, 25))
        if ratio > .8:
            pass
        elif ratio > .6:
            cowspots = cowspots[1:]
        elif ratio > .3:
            cowspots = cowspots[-2:]
        elif ratio > .2:
            cowspots = cowspots[-1:]
        else:
            cowspots = []
        for spot in cowspots:
            self.plane.blit(face, spot)
        self.plane.blit(plane_img, (0, 0))
        self.plane.set_colorkey(pg.Color("black"))
        banner = TLabel(36, "I N D I A   O R   B U S T", "maroon", "midright",
                                 self.plane_rect.left - 50, self.plane_rect.centery,
                                 "skyblue")
        self.banner_rect = banner.rect
        self.bw_surf = pg.Surface(self.banner_rect.size)
        backwards = pg.transform.flip(banner.text, True, False)
        self.bw_surf.blit(backwards, (0, 0))
        self.bw_surf.set_colorkey(pg.Color("black"))
        self.labels = []
        x = screen_rect.centerx
        msg = "You rescued {} of {} cows".format(rescued, num_cows)
        msg_label = TGLabel(self.labels, 36, msg, "gray1", "midtop", x, 50)
        leave = TGLabel(self.labels, 36, "Press SPACE for next level", "gray1",
                                "midbottom", x, screen_rect.bottom - 80)
        leave2 = TGLabel(self.labels, 36, "or ESC to exit", "gray1",
                                  "midbottom", x, leave.rect.bottom + 40)
        
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.done = True
            elif event.key == pg.K_ESCAPE:
                self.done = True            
        
    def update(self, surface, keys):
        self.plane_rect.move_ip(1, 0)
        self.banner_rect.move_ip(1, 0)
        
        self.draw(surface)
        
    def draw(self, surface):
        surface.fill(pg.Color("skyblue"))
        surface.blit(self.plane, self.plane_rect)
        surface.blit(self.bw_surf, self.banner_rect)
        for label in self.labels:
            label.display(surface)
        
        
    