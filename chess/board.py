import pygame
from .constants import SQUARE_1, SQUARE_2, ROWS, COLS, SQUARE_SIZE, BLACK, WHITE
from .piece import Piece


class Board:
    def writerow(self, row, row_num):

        temp = []
        for character in row:
            if character.isdigit():
                temp += '.'*int(character)
            else:
                temp += character

        output = []
        for col, character in enumerate(temp):
            if character == '.':
                output.append(character)
            else:
                output.append(Piece(row_num, col, character))
        
        return output


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
    
    
    def get_en_passant(self):
        if self.en_passant == '-':
            return '-'
        row = int(self.en_passant[1])
        col = 'abcdefgh'.find(self.en_passant[0])
        return (row, col)


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
    

    def get_valid(self, piece):
        coords = piece.get_pos()
        colour = piece.get_colour()
        if colour == WHITE and piece.get_piece_type() == 'Pawn':
            direction = -1
        elif colour == BLACK and piece.get_piece_type() == 'Pawn':
            direction = 1
        
        match piece.get_piece_type():
            case 'Pawn':
                moves = self._get_pawn_moves(coords, colour, direction)
            case 'Rook':
                moves = self._get_rook_moves(coords, colour) 
            case 'Knight':
                moves = self._get_knight_moves(coords, colour)
            case 'Bishop':
                moves = self._get_bishop_moves(coords, colour)
            case 'Queen':
                moves = self._get_queen_moves(coords, colour)
            case 'King':
                moves = self._get_king_moves(coords, colour) 
            
        return moves
    
    def is_on_board(self, row, col):
        if row < 0 or row >= ROWS:
            return False
        if col < 0 or col >= COLS:
            return False 
        return True
    

    def transform(self, start_pos, row_col):
        row = start_pos[0] + row_col[0] 
        col = start_pos[1] + row_col[1]
        return row, col
    

    def _traverse(self, start_coords, colour, continuos, transformations, pawn=False):
        moves = []

        for transformation in transformations:
            working_coords = start_coords

            while True:
                row, col = self.transform(working_coords, transformation)

                if not self.is_on_board(row, col):
                    break
                
                current = self.board[row][col]

                if pawn == 'diagonal' and (current == '.' or current.colour == colour):
                    break
                elif pawn == 'diagonal ' and ((row, col) == self.get_en_passant() or current.colour != colour):
                    moves.append( (row, col) )
                elif pawn == 'vert' and current != '.':
                    break
                elif current == '.':
                    moves.append( (row, col) )
                elif current.get_colour() == colour:
                    break
                elif current.get_colour() != colour:
                    moves.append( (row, col) )
                
                working_coords = (row, col)
                
                if not continuos:
                    break

        return moves
    

    def _traverse_diagonal(self, start_coords, direction, colour, continuos):
        transformations = []
        if direction != 0:
            pawn = 'diagonal'
        else:
            pawn = False
        if direction <= 0:
            transformations += [(-1,-1),(-1,1)]
        if direction >= 0:
            transformations += [(1,-1),(1,1)]
        
        return self._traverse(start_coords, colour, continuos, transformations, pawn)


    def _traverse_vertical(self, start_coords, direction, colour, continuos):
        transformations = []
        if direction != 0:
            pawn = 'vertical'
        else:
            pawn = False
        if direction <= 0:
            transformations += [(-1,0)]
        if direction >= 0:
            transformations += [(1,0)]
        
        return self._traverse(start_coords, colour, continuos, transformations, pawn)



    def _traverse_horizontal(self, start_coords, colour, continuos):
        transformations = [(0,1),(0,-1)]  
        return self._traverse(start_coords, colour, continuos, transformations, continuos)


    def _traverse_knight(self, start_coords, colour):
        moves = []
        transformations = [(1, 2) ,(-1, 2) ,(1, -2) ,(-1, -2) ,(2, 1) ,(-2, 1) ,(2, -1) ,(-2, -1)]
        moves += self._traverse(start_coords, colour, False, transformations)
        
        return moves


    def _get_pawn_moves(self, coords, colour, direction):
        moves = []
        moves += self._traverse_diagonal(coords, direction, colour, False)
        moves += self._traverse_vertical(coords, direction, colour, False)
        return moves


    def _get_rook_moves(self, coords, colour):
        moves = []
        moves += self._traverse_vertical(coords, 0, colour, True)
        moves += self._traverse_horizontal(coords, colour, True)
        return moves
    

    def _get_knight_moves(self, coords, colour):
        return self._traverse_knight(coords, colour)


    def _get_bishop_moves(self, coords, colour):
        return self._traverse_diagonal(coords, 0, colour, True)


    def _get_queen_moves(self, coords, colour):
        moves = []
        moves += self._traverse_diagonal(coords, 0, colour, True)
        moves += self._traverse_vertical(coords, 0, colour, True)
        moves += self._traverse_horizontal(coords, colour, True)
        return moves


    def _get_king_moves(self, coords, colour):
        moves = []
        moves += self._traverse_diagonal(coords, 0, colour, False)
        moves += self._traverse_vertical(coords, 0, colour, False)
        moves += self._traverse_horizontal(coords, colour, False)
        return moves


    # def winner(self):
    #     if self.red_left <= 0:
    #         return "GREEN WINS!"
    #     elif self.green_left <= 0:
    #         return "RED WINDS!"
    #     return None
