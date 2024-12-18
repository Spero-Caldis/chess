import pygame
from .constants import SQUARE_SIZE, START_FEN, VALID
from .board import Board


class Game:


    def __init__(self, win, fen):
        self._init(fen)
        self.win = win


    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)

    
    def get_info(self):
        return self.board.get_game_state_list()


    def draw_valid_moves(self, moves):
        for move in moves:
          row, col = move
          surface = pygame.Surface((SQUARE_SIZE,SQUARE_SIZE))
          surface.set_colorkey((0,0,0))  # use `(0,0,0)` (black color) as transparent color
          surface.set_alpha(128)  # transparency 50% for other colors
          pygame.draw.circle(surface, VALID, (50,50), 15)
          self.win.blit(surface, (col*SQUARE_SIZE, row*SQUARE_SIZE))


    def _init(self, fen):
        self.selected = None
        self.board = Board(fen)
        self.turn = self.board.get_turn()
        self.valid_moves = {}


    def reset(self):
        self._init()


    def done(self):
        if self.board.winner == None:
            return False
        return True

    def change_turn(self):
        self.valid_moves = {}
        self.board.change_turn()
        if self.turn == 'w':
            self.turn = 'b'
        else:
            self.turn = 'w'


    def select(self, row, col):        
        if row > 7 or col > 7:
            return False
        if self.selected and (row,col) in self.valid_moves:
            self._move(row, col)
            return

        piece = self.board.get_piece(row, col)
        if piece != '.' and piece.get_colour() == self.turn: # and self.board.get_valid(piece)
            self.selected = piece
            self.valid_moves = self.board.get_valid(piece)
            return True
        return False


    def _move(self, row, col):
        # piece = self.board.get_piece(row, col)
        if self.selected and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            self.change_turn()
            self.selected = None
            self.valid_moves = {}
        else:
            return False
        return True

#     def winner(self):
#         return self.board.winner()
