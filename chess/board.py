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
        self.castle = self.castle_string_to_list(info[2])
        self.en_passant = self.get_en_passant_coords(info[3])
        self.halfmove = info[4]
        self.fullmove = info[5]


    def get_turn(self):
        return self.turn
    
    
    def get_en_passant_coords(self, en_passant):
        if en_passant == '-':
            return False
        row = int(en_passant[1])
        col = 'abcdefgh'.find(self.en_passant[0])
        return (row, col)
    

    def get_en_passant(self):
        return self.en_passant
    

    def get_en_passant_to_remove(self):
        if not self.get_en_passant():
            return False
        if self.get_en_passant()[0] == 2:
            return (3, self.get_en_passant()[1])
        else:
            return (4, self.get_en_passant()[0])


    def set_en_passant(self, new_en_passant):
        self.en_passant = new_en_passant


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
            if self.castle[0] and self.castle[1]:
                return 'White can castle both sides'
            elif self.castle[0]:
                return 'White can castle King side'
            elif self.castle[1]:
                return 'White can castle Queen side'
            else:
                return 'White cannot castle'
        else:
            if self.caste[2] and self.castle[3]:
                return 'Black can castle both sides'
            elif self.castle[2]:
                return 'Black can castle King side'
            elif self.castle[3]:
                return 'Black can castle Queen side'
            else:
                return 'Black cannot castle'


    def castle_string_to_list(self, s):
        return ['K' in s, 'Q' in s, 'k' in s, 'q' in s]


    def get_castle(self, colour):
        if colour == WHITE:
            return (self.castle[0], self.castle[1])
        else:
            return (self.castle[2], self.castle[3])
        

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
        output += self.get_board_string() + '\n'
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
    

    def _en_passant_used(self, row, col):
        if (row, col) == self.get_en_passant():
            to_remove = self.get_en_passant_to_remove()
            self.remove(self.get_piece(to_remove[0], to_remove[1]))


    def _set_new_en_passant(self, piece : Piece, row):
        if abs(piece.get_row() - row) == 2:
            row = (piece.get_row() + row)//2
            self.set_en_passant((row, piece.get_col()))
        else:
            self.set_en_passant(False)


    def _check_en_passant(self, piece : Piece, row, col):
        if piece.get_piece_type() != 'Pawn':
            self.set_en_passant(False)
            return
        
        self._en_passant_used(row, col)
        self._set_new_en_passant(piece, row)
    
    def _do_castle(self, piece : Piece, row, col):
        if abs(piece.get_col() - col) == 2:
            if col == 6:
                self.move(self.get_piece(row, 7), row, 5)
            elif col == 2:
                self.move(self.get_piece(row, 0), row, 3)
            return True
        return False


    def _check_castle(self, piece : Piece, row, col):

        if piece.get_piece_type() == 'King':
            self._do_castle(piece, row, col)
            if piece.get_colour() == WHITE:
                self.castle[0] = False
                self.castle[1] = False
            elif piece.get_colour() == BLACK:
                self.castle[2] = False
                self.castle[3] = False

        if piece.get_piece_type() == 'Rook':
            if piece.get_colour() == WHITE:
                if piece.get_col() == 7:
                    self.castle[0] = False
                elif piece.get_col() == 0:
                    self.castle[1] = False
            elif piece.get_colour() == BLACK:
                if piece.get_col() == 7:
                    self.castle[2] = False
                elif piece.get_col() == 0:
                    self.castle[3] = False


    def _move(self, piece : Piece, row, col):
        if self.get_piece(row, col) != '.':
            self.remove(self.get_piece(row, col))
        self.board[row][col],self.board[piece.row][piece.col] = self.board[piece.row][piece.col], '.'
        piece.move(row, col)


    def move(self, piece : Piece, row, col):
        self._check_en_passant(piece, row, col)
        self._check_castle(piece, row, col)
        self._move(piece, row, col)
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
    

    def remove(self, piece : Piece):
        self.board[piece.row][piece.col] = '.'
        #TODO keep track of the chess score of each player


    def get_valid(self, piece : Piece):
        coords = piece.get_pos()
        colour = piece.get_colour()

        match piece.get_piece_type():
            case 'Pawn':
                moves = self._get_pawn_moves(coords, colour)
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
    

    def _traverse(self, start_coords, colour, continuos, transformations):
        moves = []

        for transformation in transformations:
            working_coords = start_coords

            while True:
                row, col = self.transform(working_coords, transformation)

                if not self.is_on_board(row, col):
                    break
                
                current = self.board[row][col]

                if current == '.':
                    moves.append( (row, col) )
                    working_coords = (row, col)

                elif current.get_colour() == colour:
                    break

                elif current.get_colour() != colour:
                    moves.append( (row, col) )
                    break
                
                if not continuos:
                    break

        return moves
    

    def _traverse_diagonal(self, start_coords, colour, continuos):
        transformations = [(-1,-1) ,(-1,1) ,(1,-1) ,(1,1)]
        return self._traverse(start_coords, colour, continuos, transformations)


    def _traverse_vertical(self, start_coords, colour, continuos):
        transformations = [(-1, 0), (1, 0)]
        return self._traverse(start_coords, colour, continuos, transformations)



    def _traverse_horizontal(self, start_coords, colour, continuos):
        transformations = [(0,1),(0,-1)]  
        return self._traverse(start_coords, colour, continuos, transformations)


    def _traverse_knight(self, start_coords, colour):
        moves = []
        transformations = [(1, 2) ,(-1, 2) ,(1, -2) ,(-1, -2) ,(2, 1) ,(-2, 1) ,(2, -1) ,(-2, -1)]
        moves += self._traverse(start_coords, colour, False, transformations)
        
        return moves


    def _traverse_pawn_vertical(self, start_coords, transformations):
        moves = []
        for transformation in transformations:
            row, col = self.transform(start_coords, transformation)
            current = self.board[row][col]
            if current == '.':
                moves.append( (row, col) )
        return moves


    def _traverse_pawn_diagonal(self, start_coords, colour, transformations):
        moves = []
        for transformation in transformations:
            row, col = self.transform(start_coords, transformation)
            coords = (row, col)
            current = self.board[row][col]
            en_passant = self.get_en_passant()
            if coords == en_passant:
                moves.append( coords )
            elif current == '.':
                continue
            elif current.get_colour() != colour:
                moves.append( coords ) 
        return moves




    def _traverse_castling(self, colour):
        moves = []
        castle_rights = self.get_castle(colour)
        if not castle_rights[0] and not castle_rights[1]:
            return moves
        if colour == WHITE:
            row_num = ROWS - 1
        else:
            row_num = 0

        row = self.board[row_num]
        if row[5] == row[6] == '.' and castle_rights[0]:
            moves.append((row_num, 6))
        if row[1] == row[2] == row[3] == '.' and castle_rights[1]:
            moves.append((row_num, 2))
        
        return moves


    def _get_pawn_moves(self, coords, colour):
        moves = []
        if colour == WHITE and coords[0] == 6:
            moved = False
        elif colour == BLACK and coords[0] == 1:
            moved = False
        else:
            moved = True

        if colour == WHITE and not moved:
            transformations_vertical = [(-1,0), (-2, 0)]
        elif colour == BLACK and not moved:
            transformations_vertical = [(1,0), (2, 0)]
        elif colour == WHITE:
            transformations_vertical = [(-1, 0)]
        elif colour == BLACK:
            transformations_vertical = [(1, 0)]
        
        moves += self._traverse_pawn_vertical(coords, transformations_vertical)

        if colour == WHITE:
            transformations_diagonal = [(-1,-1),(-1,1)]
        if colour == BLACK:
            transformations_diagonal = [(1,-1),(1,1)]
        moves += self._traverse_pawn_diagonal(coords, colour, transformations_diagonal)

        return moves


    def _get_rook_moves(self, coords, colour):
        moves = []
        moves += self._traverse_vertical(coords, colour, True)
        moves += self._traverse_horizontal(coords, colour, True)
        return moves
    

    def _get_knight_moves(self, coords, colour):
        return self._traverse_knight(coords, colour)


    def _get_bishop_moves(self, coords, colour):
        return self._traverse_diagonal(coords, colour, True)


    def _get_queen_moves(self, coords, colour):
        moves = []
        moves += self._traverse_diagonal(coords, colour, True)
        moves += self._traverse_vertical(coords, colour, True)
        moves += self._traverse_horizontal(coords, colour, True)
        return moves


    def _get_king_moves(self, coords, colour):
        moves = []
        moves += self._traverse_diagonal(coords, colour, False)
        moves += self._traverse_vertical(coords, colour, False)
        moves += self._traverse_horizontal(coords, colour, False)
        moves += self._traverse_castling(colour)
        return moves


    # def winner(self):
    #     if self.red_left <= 0:
    #         return "GREEN WINS!"
    #     elif self.green_left <= 0:
    #         return "RED WINDS!"
    #     return None
