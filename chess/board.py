import pygame
from .constants import SQUARE_1, SQUARE_2, ROWS, COLS, SQUARE_SIZE
from .piece import Piece

class Board:
    def writerow(self, row, row_num):
        temp = []
        for col ,piece in enumerate(row):
            if piece.isdigit():
                for j in range(int(piece)):
                    temp.append('.')
            else:
                temp.append(Piece(row_num, col, piece))
        return temp
            
    def __init__(self, fen_string):
        info = fen_string.split(' ')
        rows = info[0].split('/')
        self.board = [self.writerow(rows[x], x) for x in range(8)]
        self.turn = info[1]
        self.castle = info[2]
        self.en_passant = info[3]
        self.halfmove = info[4]
        self.fullmove = info[5]

    def get_turn(self):
        return self.turn

    def get_board_string(self):
        output = ""
        for row in self.board:
            output += ' '.join(row) + '\n'
        return output
    
    def get_turn_string(self):
        if self.turn == 'w':
            return 'White to move'
        else:
            return 'Black to move'

    def get_castle_string(self,colour):
        if colour == 'w':
            if 'KQ' in self.castle:
                return 'White can castle both sides'
            elif 'K' in self.castle:
                return 'White can castle King side'
            elif 'Q' in self.castle:
                return 'White can castle Queen side'
            else:
                return 'White cannot castle'
        else:
            if 'kq' in self.castle:
                return 'Black can castle both sides'
            elif 'k' in self.castle:
                return 'Black can castle King side'
            elif 'q' in self.castle:
                return 'Black can castle Queen side'
            else:
                return 'Black cannot castle'

    def get_en_passant_string(self):
        if self.en_passant == '-':
            return 'No en passant square'
        return 'The en passant square is: ' + self.en_passant

    def get_halfmove_string(self):
        return 'Halfmove clock: ' + str(self.halfmove)
    
    def get_fullmove_string(self):
        return 'Fullmove number: ' + str(self.fullmove)

    def get_game_state_string(self):
        output = ""
        output += self.draw_board() + '\n'
        output += self.get_turn_string() + '\n'
        output += self.get_castle_string('w') + '\n'
        output += self.get_castle_string('b') + '\n'
        output += self.get_en_passant_string() + '\n'
        output += self.get_halfmove_string() + '\n'
        output += self.get_fullmove_string()
        return output

    def __str__(self):
        output = self.get_game_state_string()
        return output

    def draw_squares(self,win):
        win.fill(SQUARE_1)
        for row in range(ROWS):
            for col in range(row % 2 , ROWS, 2):
                pygame.draw.rect(win, SQUARE_2, (row*SQUARE_SIZE , col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    def move(self, piece : Piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        
        if (row == ROWS - 1 or row == 0) and piece.get_piece_type() == 'Pawn':
            pass
            #TODO make it so pawns can become other piece when touching opposite end
    
    def get_piece(self, row, col):
        return self.board[row][col]
    
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != '.':
                    piece.draw(win)
    
    def remove(self, piece):
        self.board[piece.row][piece.col] = '.'
        #TODO keep track of the chess score of each player
    
    
    # def winner(self):
    #     if self.red_left <= 0:
    #         return "GREEN WINS!"
    #     elif self.green_left <= 0:
    #         return "RED WINDS!"
    #     return None

    # def get_valid(self, piece):
    #     moves = dict()
    #     coords = piece.get_pos()
    #     color = piece.get_color()
    #     if piece.get_king():
    #         direction = 0
    #     elif color == PLAYER_1:
    #         direction = -1
    #     elif color == PLAYER_2:
    #         direction = 1
    #     moves.update(self._traverse(coords, color, direction))

    #     return moves
    
    # def transform(self, start_pos, row_col):
    #     row = start_pos[0] + row_col[0] 
    #     col = start_pos[1] + row_col[1]
    #     return row, col

    # def is_on_board(self, row, col):
    #     if row < 0 or row >= ROWS:
    #         return False
    #     if col < 0 or col >= COLS:
    #         return False 
    #     return True
    
    # def _traverse(self, coords, color, direction):
    #     moves = {}
    #     transformations = []

    #     if direction <= 0:
    #         transformations += [(-1,-1),(-1,1)]
    #     if direction >= 0:
    #         transformations += [(1,-1),(1,1)]
        
    #     for transformation in transformations:
    #         row ,col = self.transform(coords, transformation)
    #         if not self.is_on_board(row,col):
    #             continue

    #         current = self.board[row][col]

    #         if current == 0:
    #             if self.skipped:
    #                 continue
    #             else:
    #                 moves[(row),(col)] = current
    #                 continue

    #         elif current.get_color() == color:
    #             continue

    #         row, col = self.transform((row,col),transformation)
    #         if not self.is_on_board(row,col):
    #             continue
            
    #         if self.board[row][col] == 0:
    #             moves[(row, col)] = [current]
    #     return moves
