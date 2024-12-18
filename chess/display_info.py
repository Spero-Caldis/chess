import pygame as pg
from .constants import INFO_DISPLAY_BOARDER, INFO_DISPLAY_MAIN, INFO_DISPLAY_WIDTH, HEIGHT, PADDING, TEXTCOLOUR

class DisplayInfo:
    def __init__(self, surface : pg.Surface, info):
        self.win = surface
        self.info = info
        self.update()

    
    def set_info(self, info):
        self.info = info
    
    def update(self):
        self.win.fill(INFO_DISPLAY_BOARDER)
        pg.draw.rect(self.win, INFO_DISPLAY_MAIN, (PADDING, PADDING, INFO_DISPLAY_WIDTH - 2*PADDING, (len(self.info) + 1)*PADDING*2))

        font = pg.font.Font('chess/fonts/arial.ttf', 20)

        for i, line in enumerate(self.info):
            text = font.render(line , True, TEXTCOLOUR)
            self.win.blit(text, [PADDING*2, PADDING*(2 + i*2)])