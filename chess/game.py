import pygame
from .constant import PLAYER_1, PLAYER_2, VALID, SQUARE_SIZE
from .board import Board

class Game:
    def __init__(self,win):
        self._init()
        self.win = win
    
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()
    
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = PLAYER_1
        self.valid_moves = {}

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.board.skipped:
            self.board.skipped = False
            if (row, col) in self.valid_moves:
                self._move(row, col)
            else:
                self.change_turn()
            return


        if self.selected and (row,col) in self.valid_moves:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn and self.board.get_valid(piece):
            self.selected = piece
            self.valid_moves = self.board.get_valid(piece)
            return True
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row,col)]
            if skipped:
                self.board.remove(skipped)
                self.board.skipped = True
                piece = self.board.get_piece(row, col)
                self.valid_moves = self.board.get_valid(piece)
                if not self.valid_moves:
                    self.select(0,0)
            else:
                self.change_turn()
        else:
            return False
        return True
    
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, VALID, (col*SQUARE_SIZE + SQUARE_SIZE//2, row* SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == PLAYER_1:
            self.turn = PLAYER_2
        else:
            self.turn = PLAYER_1
