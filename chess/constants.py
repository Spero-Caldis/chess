import pygame

# Drawing things on the board
WIDTH, HEIGHT = 800,800
ROWS,COLS = 8,8
INFO_DISPLAY_WIDTH = 300
PADDING = 10
SQUARE_SIZE = WIDTH//COLS
temp = round(SQUARE_SIZE*0.6)
PIECE_SIZE = (temp, temp)

#Colours
WHITE_PLAYER = (255,0,0)
BLACK_PLAYER = (255, 255, 255)
SQUARE_1 = '#5C4033' #Black squares
SQUARE_2 = '#C4A484' #White squares
INFO_DISPLAY_BOARDER = '#00008B'
INFO_DISPLAY_MAIN = '#ADD8E6'
VALID = (0,0,255) #Showing valid movements for a given piece

#Starting Fen string
START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
# START_FEN = "r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w KQkq - 0 1"


#Players
WHITE = 'w'
BLACK = 'b'

#Pieces in format 'piece code' : pygame.transform.scale(pygame.image.load('path/to/image'), (width, height))
#Uppercase means WHITE, lower case mean BLACK
# P/p = Pawn, R/r = Rook, N/n = Knight
# B/b = Bishop, Q/q = Queen, K/k = King

PIECE_SPRITES = {
#White pieces
    'P' : pygame.transform.scale(pygame.image.load('chess/assets/white_pawn.png'), PIECE_SIZE), 
    'R' : pygame.transform.scale(pygame.image.load('chess/assets/white_rook.png'), PIECE_SIZE),
    'N' : pygame.transform.scale(pygame.image.load('chess/assets/white_knight.png'), PIECE_SIZE),
    'B' : pygame.transform.scale(pygame.image.load('chess/assets/white_bishop.png'), PIECE_SIZE),
    'Q' : pygame.transform.scale(pygame.image.load('chess/assets/white_queen.png'), PIECE_SIZE),
    'K' : pygame.transform.scale(pygame.image.load('chess/assets/white_king.png'), PIECE_SIZE),
#Black pieces
    'p' : pygame.transform.scale(pygame.image.load('chess/assets/black_pawn.png'), PIECE_SIZE),
    'r' : pygame.transform.scale(pygame.image.load('chess/assets/black_rook.png'), PIECE_SIZE),
    'n' : pygame.transform.scale(pygame.image.load('chess/assets/black_knight.png'), PIECE_SIZE),
    'b' : pygame.transform.scale(pygame.image.load('chess/assets/black_bishop.png'), PIECE_SIZE),
    'q' : pygame.transform.scale(pygame.image.load('chess/assets/black_queen.png'), PIECE_SIZE),
    'k' : pygame.transform.scale(pygame.image.load('chess/assets/black_king.png'), PIECE_SIZE)
}

#Code to Name converter

CODE_TO_NAME = {
    'p' : 'Pawn',
    'r' : 'Rook',
    'n' : 'Knight',
    'b' : 'Bishop',
    'q' : 'Queen',
    'k' : 'King'
}
