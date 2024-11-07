import pygame

WIDTH,HEIGHT = 800,800
ROWS,COLS = 8,8
SQUARE_SIZE = WIDTH//COLS

#RGB
WHITE_PLAYER = (255,0,0)
BLACK_PLAYER = (255, 255, 255)
SQUARE_1 = (0,0,0) #Black squares
SQUARE_2 = (255,255,255) #White squares
VALID = (0,0,255) #Showing valid movements for a given piece
# BORDER = (128, 128, 128)
# CROWN = pygame.transform.scale(pygame.image.load('checkers/assets/crown.png'), (44,25))

#Pieces in format 'piece code' : pygame.transform.scale(pygame.image.load('path/to/image'), (width, height))
#Uppercase means WHITE, lower case mean BLACK
# P/p = Pawn, R/r = Rook, N/n = Knight
# B/b = Bishop, Q/q = Queen, K/k = King

PIECE_SPRITES = {
#White pieces
    'P' : pygame.transform.scale(pygame.image.load('chess/assets/white_pawn.png'), (60, 60)), 
    'R' : pygame.transform.scale(pygame.image.load('chess/assets/white_rook.png'), (60, 60)),
    'N' : pygame.transform.scale(pygame.image.load('chess/assets/white_knight.png'), (60, 60)),
    'B' : pygame.transform.scale(pygame.image.load('chess/assets/white_bishop.png'), (60, 60)),
    'Q' : pygame.transform.scale(pygame.image.load('chess/assets/white_queen.png'), (60, 60)),
    'K' : pygame.transform.scale(pygame.image.load('chess/assets/white_king.png'), (60, 60)),
#Black pieces
    'p' : pygame.transform.scale(pygame.image.load('chess/assets/black_pawn.png'), (60, 60)),
    'r' : pygame.transform.scale(pygame.image.load('chess/assets/black_rook.png'), (60, 60)),
    'n' : pygame.transform.scale(pygame.image.load('chess/assets/black_knight.png'), (60, 60)),
    'b' : pygame.transform.scale(pygame.image.load('chess/assets/black_bishop.png'), (60, 60)),
    'q' : pygame.transform.scale(pygame.image.load('chess/assets/black_queen.png'), (60, 60)),
    'k' : pygame.transform.scale(pygame.image.load('chess/assets/black_king.png'), (60, 60))
}

