import os
import pygame as pg
from . import tools


SCREEN_SIZE = (1080, 740)
ORIGINAL_CAPTION = "R.U.S.T.L.E.R."

pg.init()
os.environ['SDL_VIDEO_CENTERED'] = "TRUE"


SCREEN = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption(ORIGINAL_CAPTION)
SCREEN_RECT = SCREEN.get_rect()
pg.mouse.set_visible(False)

FONTS = tools.load_all_fonts(os.path.join("resources", "fonts"))
MUSIC = tools.load_all_music(os.path.join("resources", "music"))
SFX   = tools.load_all_sfx(os.path.join("resources", "sound"))
GFX   = tools.load_all_gfx(os.path.join("resources", "graphics"))
JSON = tools.load_jsons(os.path.join("resources", "json"))