import pygame
from chess.constants import WIDTH, HEIGHT, SQUARE_SIZE
from chess.game import Game

FPS = 60

WIN = pygame.display.set_mode((WIDTH + 300,HEIGHT))
pygame.display.set_caption('Chess')

BOARD = pygame.Surface((WIDTH,HEIGHT))

GAMEINFO = pygame.Surface((300, HEIGHT))


def get_row_col_from_mouse(pos):
    x,y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():
    pygame.init()
    run = True  
    clock = pygame.time.Clock()
    game = Game(BOARD)

    while run:
        clock.tick(FPS)

        #TODO Determine winner

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()
        WIN.blit(BOARD, (0, 0))
        pygame.display.update()
    
    pygame.quit()


if __name__ == '__main__':
    main()
