import pygame

WIDTH,HEIGHT = 800,800
ROWS,COLS = 8,8
SQUARE_SIZE = WIDTH//COLS

#RGB
PLAYER_1 = (255,0,0)
PLAYER_2 = (255, 255, 255)
SQUARE_1 = (0,0,0) #Black squares
SQUARE_2 = (255,255,255) #White squares
VALID = (0,0,255) #Showing valid movements for a given piece
# BORDER = (128, 128, 128)
# CROWN = pygame.transform.scale(pygame.image.load('checkers/assets/crown.png'), (44,25))

#Pieces in format 'PIECENAME' : pygame.transform.scale(pygame.image.load('path/to/image'), (width, height))

#White pieces
WHITE_PIECES_SPRITES = {
    'PAWN' : pygame.transform.scale(pygame.image.load('chess/assets/white_pawn.png'), (60, 60)),
    'ROOK' : pygame.transform.scale(pygame.image.load('chess/assets/white_rook.png'), (60, 60)),
    'KNIGHT' : pygame.transform.scale(pygame.image.load('chess/assets/white_knight.png'), (60, 60)),
    'BISHOP' : pygame.transform.scale(pygame.image.load('chess/assets/white_bishop.png'), (60, 60)),
    'QUEEN' : pygame.transform.scale(pygame.image.load('chess/assets/white_queen.png'), (60, 60)),
    'KING' : pygame.transform.scale(pygame.image.load('chess/assets/white_king.png'), (60, 60))
}

#Black pieces
BLACK_PIECES_SPRITES = {
    'PAWN' : pygame.transform.scale(pygame.image.load('chess/assets/black_pawn.png'), (60, 60)),
    'ROOK' : pygame.transform.scale(pygame.image.load('chess/assets/black_rook.png'), (60, 60)),
    'KNIGHT' : pygame.transform.scale(pygame.image.load('chess/assets/black_knight.png'), (60, 60)),
    'BISHOP' : pygame.transform.scale(pygame.image.load('chess/assets/black_bishop.png'), (60, 60)),
    'QUEEN' : pygame.transform.scale(pygame.image.load('chess/assets/black_queen.png'), (60, 60)),
    'KING' : pygame.transform.scale(pygame.image.load('chess/assets/black_king.png'), (60, 60))
}

