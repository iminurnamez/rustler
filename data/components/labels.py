import pygame as pg

from .. import prepare

                   
class MasterLabel(object):
    def __init__(self, font_size, text, text_color, rect_attribute,
                          x, y, bground_color):
        self.text = pg.font.Font(prepare.FONTS["WEST____"], font_size).render(
                                           text, False, pg.Color(text_color),
                                           pg.Color(bground_color)).convert()
        if rect_attribute == "topleft":
            self.rect = self.text.get_rect(topleft = (x, y))
        elif rect_attribute == "topright": 
            self.rect = self.text.get_rect(topright = (x, y))
        elif rect_attribute == "bottomleft": 
            self.rect = self.text.get_rect(bottomleft = (x, y))
        elif rect_attribute == "bottomright": 
            self.rect = self.text.get_rect(bottomright = (x, y))
        elif rect_attribute == "midtop":
            self.rect = self.text.get_rect(midtop = (x, y))
        elif rect_attribute == "midbottom": 
            self.rect = self.text.get_rect(midbottom = (x, y))
        elif rect_attribute == "center": 
            self.rect = self.text.get_rect(center = (x, y))
        elif rect_attribute == "midleft": 
            self.rect = self.text.get_rect(midleft = (x, y))
        elif rect_attribute == "midright": 
            self.rect = self.text.get_rect(midright = (x, y))

    def draw(self, surface):
        surface.blit(self.text, self.rect)

class Label(MasterLabel):
    def __init__(self, font_size, text, text_color, rect_attribute,
                          x, y, bground_color="black"):
        super(Label, self).__init__(font_size, text, text_color, rect_attribute,
                          x, y, bground_color)

       
class GroupLabel(MasterLabel):                             
    def __init__(self, group, font_size, text, text_color, rect_attribute,
                          x, y, bground_color="black"):
        super(GroupLabel, self).__init__(font_size, text, text_color, rect_attribute,
                          x, y, bground_color)
        group.append(self)

        
class TransparentLabel(Label):
    def __init__(self, font_size, text, text_color, rect_attribute,
                          x, y, bground_color="black"):
        super(TransparentLabel, self).__init__(font_size, text, text_color, rect_attribute,
                          x, y, bground_color)
        self.surface = pg.Surface(self.rect.size)
        self.surface.set_colorkey(pg.Color(bground_color))
        self.surface.blit(self.text, (0, 0))

    def draw(self, surface):
        surface.blit(self.surface, self.rect)


class TransparentGroupLabel(TransparentLabel):
    def __init__(self, group, font_size, text, text_color, rect_attribute,
                          x, y, bground_color="black"):
        super(TransparentGroupLabel, self).__init__(font_size, text, text_color,
                                                               rect_attribute, x, y, bground_color)
        self.surface = pg.Surface(self.rect.size)
        self.surface.set_colorkey(pg.Color(bground_color))
        self.surface.blit(self.text, (0, 0))
        group.append(self)
