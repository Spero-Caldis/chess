import pygame
from chess.constants import WIDTH, HEIGHT, SQUARE_SIZE, INFO_DISPLAY_WIDTH, START_FEN
from chess.game import Game
from chess.display_info import DisplayInfo
import sys

FPS = 60

WIN = pygame.display.set_mode((WIDTH + INFO_DISPLAY_WIDTH ,HEIGHT))
pygame.display.set_caption('Chess')

BOARD = pygame.Surface((WIDTH,HEIGHT))
INFODISPLAY = pygame.Surface((INFO_DISPLAY_WIDTH , HEIGHT))


def get_row_col_from_mouse(pos):
    x,y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def get_fen():
    try:
        fen = sys.argv[1]
        return fen
    except IndexError:
        print('No fen string provided, using start string')
        return START_FEN



def main():
    fen = get_fen()
    pygame.init()
    run = True  
    clock = pygame.time.Clock()
    game = Game(BOARD, fen)
    info_display = DisplayInfo(INFODISPLAY, game.get_info())

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if game.done():
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()
        WIN.blit(BOARD, (0, 0))
        
        info_display.set_info(game.get_info())
        info_display.update()
        WIN.blit(INFODISPLAY, (WIDTH, 0))

        pygame.display.update()
    
    pygame.quit()


if __name__ == '__main__':
    main()
