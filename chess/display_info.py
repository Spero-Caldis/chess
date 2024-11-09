import pygame
from .constants import INFO_DISPLAY_BOARDER, INFO_DISPLAY_MAIN, INFO_DISPLAY_WIDTH, HEIGHT, PADDING

class DisplayInfo:
    def __init__(self, surface : pygame.Surface, info):
        self.win = surface
        self.turn = info[0]
        self.halfmove = info[1]
        self.fullmove = info[2]
        self.update()
    
    def update(self):
        self.win.fill(INFO_DISPLAY_BOARDER)
        pygame.draw.rect(self.win, INFO_DISPLAY_MAIN, (PADDING, PADDING, INFO_DISPLAY_WIDTH - 2*PADDING, HEIGHT - 2*PADDING))
        # text = font.render("Score: " + str(self.score), True, WHITE)
        # self.display.blit(text, [0, 0])