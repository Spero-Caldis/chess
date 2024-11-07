import pygame
from .constant import SQUARE_1, SQUARE_2, ROWS, COLS, PLAYER_1, PLAYER_2, SQUARE_SIZE
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.red_left = 12
        self.green_left = 12
        self.red_kings = 0
        self.green_kings = 0
        self.skipped = False
        self.create_board()

    def draw_squares(self,win):
        win.fill(SQUARE_1)
        for row in range(ROWS):
            for col in range(row % 2 , ROWS, 2):
                pygame.draw.rect(win, SQUARE_2, (row*SQUARE_SIZE , col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        
        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == PLAYER_2:
                self.green_kings += 1
            else:
                self.red_kings += 1
    
    def get_piece(self, row, col):
        return self.board[row][col]


    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, PLAYER_2))  
                    elif row > 4:

                        self.board[row].append(Piece(row, col, PLAYER_1))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)
    
    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == PLAYER_1:
                    self.red_left -= 1
                else:
                    self.green_left -= 1
    
    def winner(self):
        if self.red_left <= 0:
            return "GREEN WINS!"
        elif self.green_left <= 0:
            return "RED WINDS!"
        return None

    def get_valid(self, piece):
        moves = dict()
        coords = piece.get_pos()
        color = piece.get_color()
        if piece.get_king():
            direction = 0
        elif color == PLAYER_1:
            direction = -1
        elif color == PLAYER_2:
            direction = 1
        moves.update(self._traverse(coords, color, direction))

        return moves
    
    def transform(self, start_pos, row_col):
        row = start_pos[0] + row_col[0] 
        col = start_pos[1] + row_col[1]
        return row, col

    def is_on_board(self, row, col):
        if row < 0 or row >= ROWS:
            return False
        if col < 0 or col >= COLS:
            return False 
        return True
    
    def _traverse(self, coords, color, direction):
        moves = {}
        transformations = []

        if direction <= 0:
            transformations += [(-1,-1),(-1,1)]
        if direction >= 0:
            transformations += [(1,-1),(1,1)]
        
        for transformation in transformations:
            row ,col = self.transform(coords, transformation)
            if not self.is_on_board(row,col):
                continue

            current = self.board[row][col]

            if current == 0:
                if self.skipped:
                    continue
                else:
                    moves[(row),(col)] = current
                    continue

            elif current.get_color() == color:
                continue

            row, col = self.transform((row,col),transformation)
            if not self.is_on_board(row,col):
                continue
            
            if self.board[row][col] == 0:
                moves[(row, col)] = [current]
        return moves
