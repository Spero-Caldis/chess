import pygame
from .constants import SQUARE_SIZE, START_FEN, VALID
from .board import Board


class Game:


    def __init__(self,win):
        self._init()
        self.win = win


    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()


    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, VALID, (col*SQUARE_SIZE + SQUARE_SIZE//2, row* SQUARE_SIZE + SQUARE_SIZE // 2), 15)


    def _init(self):
        self.selected = None
        self.board = Board(START_FEN)
        self.turn = self.board.get_turn()
        self.valid_moves = {}


    def reset(self):
        self._init()


    def change_turn(self):
        self.valid_moves = {}
        if self.turn == 'w':
            self.turn = 'b'
        else:
            self.turn = 'w'


    def select(self, row, col):        
        if self.selected and (row,col) in self.valid_moves:
            self._move(row, col)
            return

        piece = self.board.get_piece(row, col)
        if piece != '.' :#and piece.get_colour() == self.turn: # and self.board.get_valid(piece)
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
