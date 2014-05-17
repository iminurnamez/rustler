from random import randint, uniform
from math import degrees, pi
from itertools import chain
import pygame as pg
from ..import tools, prepare
from ..components import cows, cowboy, obstacles, wolf, lasso, spawner, level
from ..components.labels import Label, TransparentLabel as TLabel


class Game(tools._State):
    def __init__(self):
        super(Game, self).__init__()
        self.done = False
        self.fps = 60
        self.font = pg.font.Font(prepare.FONTS["WEST____"], 24)
        self.screen_rect = pg.display.get_surface().get_rect()
        self.level_num = 1
        self.levels = level.levels
        self.level = self.levels[self.level_num]
         
        self.class_map = {"grass": (obstacles.Grass, None),
                                   "cactus": (obstacles.Cactus, None),
                                   "smallrock": (obstacles.SmallRock, None),
                                   "bigrock": (obstacles.BigRock, None),
                                   "fencevert": (obstacles.Fence, "vert"),
                                   "fencehoriz": (obstacles.Fence, "horiz"),
                                   "airstrip": (obstacles.Airstrip, None)}
        
        self.whip_sound = prepare.SFX["whip_sound"]    
        self.load_level(self.level)

        
    def startup(self, persistent):
        self.persist = persistent
        pg.display.set_caption(self.level.title)

        
    def load_level(self, level):
        self.width = level.width
        self.height = level.height
        self.num_cows = level.num_cows
        x_low, x_high = level.cow_rangex
        y_low, y_high = level.cow_rangey
        if level.cow_angle == "random":
            self.cows = [cows.Cow((randint(x_low, x_high), randint(y_low, y_high)), uniform(0, pi * 2)) for _ in range(self.num_cows)]
        else:
            self.cows = [cows.Cow((randint(x_low, x_high), randint(y_low, y_high)), level.cow_angle) for _ in range(self.num_cows)]
        self.cowboy = cowboy.Cowboy(level.cowboy_pos)
        self.lasso = None
        self.total_offset = (0, 0)
        self.obstacles = []
        self.wolf_spawners = []
        centerx = 5
        centery = 32
        for i in range(int(self.height / 64)):
            self.obstacles.append(obstacles.Fence((centerx, centery), "vert"))
            self.obstacles.append(obstacles.Fence((centerx + self.width, centery), "vert"))
            centery += 64
        centerx = 37
        centery = 5
        for j in range(int(self.width / 64)):
            self.obstacles.append(obstacles.Fence((centerx, centery), "horiz"))
            self.obstacles.append(obstacles.Fence((centerx, centery + self.height), "horiz"))
            centerx += 64
        for obst in prepare.JSON[level.obst_json]:
            if str(obst[1]) == "wolfspawner":
                self.wolf_spawners.append(spawner.WolfSpawner((obst[0][0], obst[0][1])))
            else:
                self.obstacles.append(self.class_map[str(obst[1])][0]((obst[0][0], obst[0][1]),
                                                self.class_map[obst[1]][1]))
        
        hw = self.width/2.0
        hh = self.height / 2.0
        self.topleft_obstacles = [x for x in self.obstacles if x.pos[0] <= hw and x.pos[1] <= hh]
        self.topright_obstacles = [x for x in self.obstacles if x.pos[0] > hw and x.pos[1] <= hh]
        self.bottomleft_obstacles = [x for x in self.obstacles if x.pos[0] <= hw and x.pos[1] > hh]
        self.bottomright_obstacles = [x for x in self.obstacles if x.pos[0] > hw and x.pos[1] > hh]
        
        self.obstacles = sorted(self.obstacles, key=lambda x: x.rect.centery)
        self.wolves = []
        self.bullets = []
        self.rescued = 0
        x_move =  self.screen_rect.centerx - self.cowboy.pos[0]
        y_move =  self.screen_rect.centery - self.cowboy.pos[1]
        self.move_all(x_move, y_move)
        self.cowboy.move((x_move, y_move))
        self.start_time = pg.time.get_ticks()
        
                
        
    def end_level(self):
        self.persist["num cows"] = self.num_cows
        self.persist["rescued"] = self.rescued
        self.persist["time"] = pg.time.get_ticks() - self.start_time
        self.next = "ENDSCREEN"
        self.done = True
        
        try:
            self.level = self.levels[self.level_num + 1]
            self.level_num += 1
        except KeyError:
            pass
        self.load_level(self.level)
            
            
    def accelerate_cows(self, increment):
        self.whip_sound.play()
        collision_rect = pg.Rect(0, 0, 320, 320)
        collision_rect.center = self.cowboy.pos
        for cow in [x for x in self.cows if collision_rect.collidepoint(x.pos)]:
            cow.boost += increment
            if cow.boost > cow.max_boost:
                cow.boost = cow.max_boost
                
    def world_map(self):
        offset =self.total_offset
        map_surf = pg.Surface(self.screen_rect.size)
        map_surf.fill(pg.Color("tan"))
        pg.draw.rect(map_surf, pg.Color("gray1"), map_surf.get_rect(), 2)
        for obst in chain(self.obstacles, self.cows, self.wolves):
            obst.draw_icon(map_surf, offset)            
        self.cowboy.draw_icon(map_surf, offset)
        return map_surf
        
        
    def move_all(self, x_move, y_move):    
        for thing in chain(self.cows, self.obstacles, self.wolves, self.wolf_spawners):
            thing.move(( x_move, y_move))
        self.total_offset = (self.total_offset[0] - x_move, self.total_offset[1] - y_move)
    
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
                self.cowboy.shoot(self.bullets)
            elif event.key == pg.K_s:
                if not self.lasso:
                    self.lasso = lasso.Lasso(self.cowboy)
                else:
                    self.lasso.get_event(event)                
            elif event.key == pg.K_ESCAPE:
                self.end_level()           
                
    def draw_ui(self, surface):
        label = self.font.render("{:10}{}".format("Cows", len(self.cows)), True, pg.Color("gray1"), pg.Color("black"))
        label.set_colorkey(pg.Color("black"))
        surface.blit(label, (10, 10))        
        #TLabel(24, "{:10}{}".format("Cows", len(self.cows)),
        #           "white", "topleft", 10, 10, "gray1").draw(surface)
     
        
    
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
            x = self.total_offset[0] + cow.pos[0]
            y = self.total_offset[1] + cow.pos[1]
            hw = self.width / 2.0
            hh = self.height / 2.0
            if x <= hw and y <= hh:
                obst_list = self.topleft_obstacles
            elif x > hw and y <= hh:
                obst_list = self.topright_obstacles
            elif  x <= hw and y > hh:
                obst_list = self.bottomleft_obstacles
            elif  x > hw and y > hh:
                obst_list = self.bottomright_obstacles
            cow.update(self.cows, obst_list)
        
        for c in self.cows:
            c.move_turn()
        
        self.cowboy.move_turn()
        
        for bullet in self.bullets:
            bullet.update(self.wolves, self.cows, self.obstacles)
        self.bullets = [x for x in self.bullets if not x.done]
        self.wolves = [x for x in self.wolves if x.health > 0]
        rescued = [x for x in self.cows if x.rescued]
        self.rescued += len(rescued)
        for a_cow in [x for x in self.cows if (x.health <= 0) or (x.belly <= 0)]:
            self.obstacles.append(obstacles.Carcass(a_cow.angle, a_cow.pos))
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
            
        x_move = x_offset * self.cowboy.speed * 2
        y_move = y_offset * self.cowboy.speed * 2
        self.move_all(x_move, y_move)
        self.cowboy.move((x_move, y_move))
    
        
        self.ground_level = []
        self.upright = []
        everything = chain([x for x in self.obstacles if x.rect.colliderect(self.screen_rect)],
                                     self.cows, self.wolves, [self.cowboy])
        for e in everything:
            if e.name in ("grass", "airstrip") or ("fence" in e.name):
                self.ground_level.append(e)
            else:
                self.upright.append(e)
        self.upright = sorted(self.upright, key=lambda x: x.rect.bottom) 
        self.draw(surface)
        if len(self.cows) < 1:
            self.end_level()
        
    def draw(self, surface):
        surface.fill(pg.Color("tan"))
        
        for item in chain(self.ground_level, self.upright):
            item.draw(surface)
        for bullet in self.bullets:
            bullet.draw(surface)
        if self.lasso:
            self.lasso.draw(surface)
        self.draw_ui(surface)
        
        
    