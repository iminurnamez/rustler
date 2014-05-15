from random import randint
from itertools import chain
import pygame as pg
from ..import tools, prepare
from ..components import cows, cowboy, obstacles, wolf, lasso, spawner
from ..components.labels import Label, TransparentLabel as TLabel


class Game(tools._State):
    def __init__(self):
        super(Game, self).__init__()
        self.done = False
        self.fps = 60
        self.screen_rect = pg.display.get_surface().get_rect()
        
        
        
        
        self.width, self.height = 2000, 2000
        
        self.num_cows = 30
        self.cows = [cows.Cow((randint(100, 500), randint(100, 500))) for _ in range(self.num_cows)]
        self.cowboy = cowboy.Cowboy((400, 400))
        self.lasso = None
        self.total_offset = (0, 0)
        self.class_map = {"grass": (obstacles.Grass, None),
                                   "cactus": (obstacles.Cactus, None),
                                   "smallrock": (obstacles.SmallRock, None),
                                   "bigrock": (obstacles.BigRock, None),
                                   "fencevert": (obstacles.Fence, "vert"),
                                   "fencehoriz": (obstacles.Fence, "horiz"),
                                   "airstrip": (obstacles.Airstrip, None)}
                        
        self.obstacles = []
        self.wolf_spawners = []
        centerx = 5
        centery = 32
        for i in range(self.height / 64):
            self.obstacles.append(obstacles.Fence((centerx, centery), "vert"))
            centery += 64
        centerx = 37
        centery = 5
        for j in range(self.width / 64):
            self.obstacles.append(obstacles.Fence((centerx, centery), "horiz"))
            centerx += 64
        for obst in prepare.JSON["obstacles"]:
            if str(obst[1]) == "wolfspawner":
                self.wolf_spawners.append(spawner.WolfSpawner((obst[0][0], obst[0][1])))
            else:
                self.obstacles.append(self.class_map[str(obst[1])][0]((obst[0][0], obst[0][1]),
                                                 self.class_map[obst[1]][1]))
        
        self.obstacles = sorted(self.obstacles, key=lambda x: x.rect.centery)
        self.wolves = []
        self.bullets = []
        
        #TODO - Level object
        self.rescued = 0
        self.rescue_goal = 10
        
        self.whip_sound = prepare.SFX["whip_sound"]
        
    def end_level(self):
        self.persist["num cows"] = self.num_cows
        self.persist["rescued"] = self.rescued
        self.next = "ENDSCREEN"
        self.done = True
        #self.level_num += 1
        #try:
        #    self.level = self.levels[self.level_num]
        #except KeyError:
        #    pass
            
    def accelerate_cows(self, increment):
        self.whip_sound.play()
        collision_rect = pg.Rect(0, 0, 264, 264)
        collision_rect.center = self.cowboy.pos
        for cow in [x for x in self.cows if x.rect.colliderect(collision_rect)]:
            cow.boost += increment
            if cow.boost > cow.max_boost:
                cow.boost = cow.max_boost
                
    def world_map(self):
        offset = self.total_offset
        map_surf = pg.Surface(self.screen_rect.size)
        map_surf.fill(pg.Color("tan"))
        pg.draw.rect(map_surf, pg.Color("gray1"), map_surf.get_rect(), 2)
        for obst in chain(self.obstacles, self.cows, self.wolves):
            obst.draw_icon(map_surf, offset)            
        self.cowboy.draw_icon(map_surf, offset)
        return map_surf
        
        
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.end_level()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                self.accelerate_cows(.5)
            elif event.key == pg.K_m:
                self.persist["worldmap"] = self.world_map()
                self.next = "WORLDMAP"
                self.done = True
            elif event.key == pg.K_SPACE:
                if self.lasso:
                    self.lasso.get_event(event)
                    
                else:
                    self.cowboy.shoot(self.bullets)
            elif event.key == pg.K_l:
                if not self.lasso:
                    self.lasso = lasso.Lasso(self.cowboy)
            elif event.key == pg.K_ESCAPE:
                self.end_level()           
                
    def draw_ui(self, surface):
        cows = TLabel(24, "{:10}{}".format("Cows", len(self.cows)),
                              "white", "topleft", 10, 10, "gray1")
        rescued = TLabel(24, "{:10}{}/{}".format("Rescued",
                                  self.rescued, self.rescue_goal),
                                  "white", "topleft", cows.rect.left, 
                                  cows.rect.bottom + 10, "gray1")        
        cows.display(surface)
        rescued.display(surface)
    
    def update(self, surface, keys):
        if keys[pg.K_LEFT]:
            self.cowboy.angle += self.cowboy.turn_speed
        elif keys[pg.K_RIGHT]:
            self.cowboy.angle -= self.cowboy.turn_speed
        if keys[pg.K_UP]:
            self.cowboy.accelerate(1)
        if keys[pg.K_DOWN]:
            self.cowboy.accelerate(-1)
            
        for spawner in self.wolf_spawners:
            spawner.update(self.wolves)
        
        self.cowboy.update(self.cows, self.obstacles)
        if self.lasso:
            self.lasso.update(self.cows, self.wolves)
            if self.lasso.done:
                self.lasso = None
        for wolf in self.wolves:
            wolf.update(self.cows, self.obstacles)
        for cow in self.cows:
            cow.update(self.cows, self.obstacles)
        
        for c in self.cows:
            c.move_turn()
        
        self.cowboy.move_turn()
        
        for bullet in self.bullets:
            bullet.update(self.wolves, self.cows, self.obstacles)
        self.bullets = [x for x in self.bullets if not x.done]
        self.wolves = [x for x in self.wolves if x.health > 0]
        rescued = [x for x in self.cows if x.rescued]
        self.rescued += len(rescued)
        self.cows = [x for x in self.cows if (x.health > 0 and x.belly > 0) and not x.rescued]
        
        x_offset, y_offset = 0, 0
        if self.cowboy.pos[0] < 250:
            x_offset = 1
        elif self.cowboy.pos[0] > self.screen_rect.right - 250:
            x_offset = -1
        if self.cowboy.pos[1] < 250:
            y_offset = 1
        elif self.cowboy.pos[1] > self.screen_rect.bottom -250:
            y_offset = -1
        if x_offset or y_offset:    
            x_move = x_offset * self.cowboy.speed * 2
            y_move = y_offset * self.cowboy.speed * 2
            for thing in chain(self.cows, self.obstacles, self.wolves, self.wolf_spawners, [self.cowboy]):
                thing.move(( x_move, y_move))
            self.total_offset = (self.total_offset[0] - x_move, self.total_offset[1] - y_move)
        self.draw(surface)
        
        
    def draw(self, surface):
        surface.fill(pg.Color("tan"))
        everything = chain([x for x in self.obstacles if x.rect.colliderect(self.screen_rect)],
                                     self.cows, self.wolves, [self.cowboy])
        everything = sorted(everything, key= lambda x: x.rect.bottom)
        for e in everything:
            e.draw(surface)
        
        
        for bullet in self.bullets:
            bullet.draw(surface)
        if self.lasso:
            self.lasso.draw(surface)
        self.draw_ui(surface)
        #TESTING
        for spawner in self.wolf_spawners:
            pg.draw.rect(surface, pg.Color("purple"), (spawner.pos[0] - 10, spawner.pos[1] - 10, 20, 20))
        
    