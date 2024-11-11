import pygame
from .constants import SQUARE_1, SQUARE_2, ROWS, COLS, SQUARE_SIZE, BLACK, WHITE, CODE_TO_NAME
from .piece import Piece
from .evolvepawn import EvolvePawn


class Board:


    """
    __x__ type functions
    """
    def __init__(self, fen_string):
            info = fen_string.split(' ')
            rows = info[0].split('/')
            self.board = [self.writerow(rows[x], x) for x in range(8)]
            self.turn = info[1]
            self.castle = self.castle_string_to_list(info[2])
            self.en_passant = self.string_to_coords(info[3])
            self.halfmove = int(info[4])
            self.fullmove = int(info[5])
            self.winner = None


    def __str__(self):
        output = self.get_game_state_string()
        return output


    """
    Accessor methods
    """

    def get_turn(self):
        return self.turn
    

    def get_en_passant(self):
        return self.en_passant
    

    def get_en_passant_to_remove(self):
        if not self.get_en_passant():
            return False
        if self.get_en_passant()[0] == 2:
            return (3, self.get_en_passant()[1])
        else:
            return (4, self.get_en_passant()[1])


    def get_board_list(self):
        output = []
        for row in self.board:
            temp = []
            for item in row:
                if item == '.':
                    temp.append('.')
                elif type(item) == Piece:
                    temp.append(item.get_piece_code())                
            output.append(temp)
        return output
    

    def get_board_string(self):
        board_list = self.get_board_list()
        output = ''
        for row in board_list:
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
            if self.castle[2] and self.castle[3]:
                return 'Black can castle both sides'
            elif self.castle[2]:
                return 'Black can castle King side'
            elif self.castle[3]:
                return 'Black can castle Queen side'
            else:
                return 'Black cannot castle'


    def get_en_passant_string(self):
        if self.en_passant == False:
            return 'No en passant square'
        return 'The en passant square is: ' + self.coords_to_string(self.en_passant)


    def get_halfmove_string(self):
        return 'Halfmove clock: ' + str(self.halfmove)


    def get_fullmove_string(self):
        return 'Fullmove number: ' + str(self.fullmove)


    def get_game_state_string(self):
        output = ""
        # output += self.get_board_string() + '\n'
        output += self.get_turn_string() + '\n'
        output += self.get_castle_string('w') + '\n'
        output += self.get_castle_string('b') + '\n'
        output += self.get_en_passant_string() + '\n'
        output += self.get_halfmove_string() + '\n'
        output += self.get_fullmove_string()
        return output


    def get_king_pos(self, colour, board=False):
        board = self._check_board_given(board)
        if colour == WHITE:
            king = 'K'
        else:
            king = 'k'
        for row_num, row in enumerate(board):
            for col_num, piece in enumerate(row):
                if piece == king:
                    return (row_num, col_num)
        return False


    def get_king_is_checked_string(self, colour):
        if colour == WHITE:
            colour_out = 'White'
        else:
            colour_out = 'Black'

        king_coords = self.get_king_pos(colour)
        checked_state = self._king_is_checked(king_coords, colour)
        

        if checked_state:
            return f'{colour_out} is under check'
        return f'The {colour_out} is not under check'


    def get_game_state_list(self):
        output = []
        output.append(self.get_turn_string())
        output.append(self.get_castle_string('w'))
        output.append(self.get_castle_string('b'))
        output.append(self.get_en_passant_string())
        output.append(self.get_halfmove_string())
        output.append(self.get_fullmove_string())
        output.append(self.get_king_is_checked_string(WHITE))
        output.append(self.get_king_is_checked_string(BLACK))
        if self.winner == WHITE:
            output.append('White has won the game!')
        elif self.winner == BLACK:
            output.append('Black has won the game!')
        return output


    def get_board_as_fen(self):
        board = self.get_board_list()
        output = []
        count = 0
        for row in board:
            temp = ''
            for piece in row:
                if piece != '.' and count == 0:
                    temp += piece
                elif piece == '.':
                    count += 1
                elif piece != '.':
                    temp += str(count)
                    count = 0
                    temp += piece
            if count != 0:
                temp += str(count)
                count = 0
            output.append(temp)
        return '/'.join(output)
    

    def get_castle(self, colour):
        if colour == WHITE:
            return (self.castle[0], self.castle[1])
        else:
            return (self.castle[2], self.castle[3])


    def get_castle_as_fen(self):
        temp = 'KQkq'
        output = ''
        for i, can_castle in enumerate(self.castle):
            if can_castle:
                output += temp[i]
        if len(output) == 0:
            return '-'
        return output


    def get_piece(self, row, col):
        return self.board[row][col]


    def get_fen(self):
        board = self.get_board_as_fen()
        turn = self.get_turn()
        castle_rights = self.get_castle_as_fen()
        en_passant = self.coords_to_string(self.get_en_passant())
        halfmove = str(self.halfmove)
        fullmove = str(self.fullmove)
        fen = ' '.join([board, turn, castle_rights, en_passant, halfmove, fullmove])
        return fen


    """
    Mutator methods
    """
    def _move(self, piece : Piece, row, col):
        if self.get_piece(row, col) != '.':
            self.remove(self.get_piece(row, col))
            self.halfmove = 0
        self.board[row][col],self.board[piece.row][piece.col] = self.board[piece.row][piece.col], '.'
        piece.move(row, col)


    def move(self, piece : Piece, row, col):
        self.halfmove += 1
        if piece.get_piece_type() == 'Pawn':
            self.halfmove = 0
        self._check_en_passant(piece, row, col)
        self._check_castle(piece, row, col)
        self._move(piece, row, col)
        if (row == ROWS - 1 or row == 0) and piece.get_piece_type() == 'Pawn':
            temp = []
            EvolvePawn(temp)
            new_piece_code = temp[0]
            if piece.get_colour() == WHITE:
                new_piece_code = new_piece_code.upper()
            piece.change_piece_type(new_piece_code)


    def _set_new_en_passant(self, piece : Piece, row):
        if abs(piece.get_row() - row) == 2:
            row = (piece.get_row() + row)//2
            self.set_en_passant((row, piece.get_col()))
        else:
            self.set_en_passant(False)


    def remove(self, piece : Piece):
        self.board[piece.row][piece.col] = '.'
        #TODO keep track of the chess score of each player


    def set_en_passant(self, new_en_passant):
        self.en_passant = new_en_passant


    def _do_castle(self, piece : Piece, row, col):
        if abs(piece.get_col() - col) == 2:
            if col == 6:
                self.move(self.get_piece(row, 7), row, 5)
            elif col == 2:
                self.move(self.get_piece(row, 0), row, 3)
            return True
        return False


    def _en_passant_used(self, row, col):
        if (row, col) == self.get_en_passant():
            to_remove = self.get_en_passant_to_remove()
            self.remove(self.get_piece(to_remove[0], to_remove[1]))


    def change_turn(self):
        self.check_for_winner()
        if self.turn == 'w':
            self.turn = 'b'
        else:
            self.turn = 'w'
            self.fullmove += 1
        print(self.get_fen())


    """
    Converter methods
    """
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


    def castle_string_to_list(self, s):
        return ['K' in s, 'Q' in s, 'k' in s, 'q' in s]


    def string_to_coords(self, string):
        if string == '-':
            return False
        col = 'abcdefgh'.find(string[0])
        row = (8-int(string[1]))
        return (row, col)


    def coords_to_string(self, coords):
        if not coords:
            return '-'
        row = str(8 - coords[0])
        col = 'abcdefgh'[coords[1]]
        return col + row


    def transform(self, start_pos, row_col):
        row = start_pos[0] + row_col[0] 
        col = start_pos[1] + row_col[1]
        return row, col
 

    def code_to_colour(self, piece_code):
        if piece_code == '.':
            return False
        if piece_code.upper() == piece_code:
            return WHITE
        return BLACK

    """
    Graphical methods
    """
    def draw_squares(self,win):
        win.fill(SQUARE_1)
        for row in range(ROWS):
            for col in range(row % 2 , ROWS, 2):
                pygame.draw.rect(win, SQUARE_2, (row*SQUARE_SIZE , col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != '.':
                    piece.draw(win)
 

    """
    Checker methods
    """
    def _check_en_passant(self, piece : Piece, row, col):
        if piece.get_piece_type() != 'Pawn':
            self.set_en_passant(False)
            return
        
        self._en_passant_used(row, col)
        self._set_new_en_passant(piece, row)
    

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
   

    def is_on_board(self, row, col):
        if row < 0 or row >= ROWS:
            return False
        if col < 0 or col >= COLS:
            return False 
        return True
 

    def _check_board_given(self, board):
        if not board:
            output = self.get_board_list()
        else:
            output = board
        return output


    def _check_coords_for_pieces(self, colour, board, coords : list, pieces : list):
        if colour == BLACK:
            pieces = [x.upper() for x in pieces]
        for row, col in coords:
            if board[row][col] in pieces:
                return (row, col)
        return False


    def _king_is_checked(self, king_coords, colour, board=False):
        checker = self._check_coords_for_pieces
        board = self._check_board_given(board)

        moves = self._traverse_pawn_diagonal(king_coords, colour, board)
        output = checker(colour, board, moves, ['p'])
        if output:        #Checking if pawn is holding king under check
            return output
        
        moves = self._traverse_diagonal(king_coords, colour, True, board)
        output = checker(colour, board, moves, ['b','q'])
        if output:    #Checking if bishop or queen is holding king under check
            return output
        
        moves = self._traverse_vertical(king_coords, colour, True, board)
        moves += self._traverse_horizontal(king_coords, colour, True, board)
        output = checker(colour, board, moves, ['r','q'])
        if output:    #Checking if rook or queen is holding king under check
            return output
        

        moves = self._traverse_knight(king_coords, colour, board)
        output = checker(colour, board, moves, ['n'])
        if output:        #Checking if knight is holding king under check
            return output
        
        moves = self._traverse_diagonal(king_coords, colour, False, board)
        moves += self._traverse_vertical(king_coords, colour, False, board)
        moves += self._traverse_horizontal(king_coords, colour, False, board)
        output = checker(colour, board, moves, ['k'])
        if output:        #Checking if king is holding king under check
            return output
        
        return False


    def check_mate(self, colour):
        board = self.board  
        possible_moves = []
        for row in board:
            for piece in row:
                if piece == '.':
                    continue
                elif piece.get_colour() == colour:
                    possible_moves += self.get_valid(piece)
        if len(possible_moves) == 0:
            return True
        return False


    def check_for_winner(self):
        if self.check_mate(WHITE):
            self.winner = BLACK
            return BLACK
        elif self.check_mate(BLACK):
            self.winner = WHITE
            return WHITE
        if self.halfmove == 50:
            self.winner = 'TIE'
            return 'TIE'
        return None


    """
    Finding valid moves methods
    """

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

        start_board = self.get_board_list()
        piece = start_board[coords[0]][coords[1]]
        start_board[coords[0]][coords[1]] = '.'

        valid_moves = []

        for row, col in moves:
            working_board = [x.copy() for x in start_board]
            working_board[row][col] = piece
            king_coords = self.get_king_pos(colour,working_board)
            output = self._king_is_checked(king_coords, colour, working_board)
            if not output:
                valid_moves.append((row, col))
        return valid_moves


    def _traverse(self, start_coords, colour, continuos, transformations, board):
        moves = []

        for transformation in transformations:
            working_coords = start_coords

            while True:
                row, col = self.transform(working_coords, transformation)

                if not self.is_on_board(row, col):
                    break
                
                current = board[row][col]

                if current == '.':
                    moves.append( (row, col) )
                    working_coords = (row, col)

                elif self.code_to_colour(current) == colour:
                    break

                elif self.code_to_colour(current) != colour:
                    moves.append( (row, col) )
                    break
                
                if not continuos:
                    break

        return moves
    

    def _traverse_diagonal(self, start_coords, colour, continuos, board=False):
        board = self._check_board_given(board)
        transformations = [(-1,-1) ,(-1,1) ,(1,-1) ,(1,1)]
        return self._traverse(start_coords, colour, continuos, transformations, board)


    def _traverse_vertical(self, start_coords, colour, continuos, board=False):
        board = self._check_board_given(board)
        transformations = [(-1, 0), (1, 0)]
        return self._traverse(start_coords, colour, continuos, transformations, board)


    def _traverse_horizontal(self, start_coords, colour, continuos, board=False):
        board = self._check_board_given(board)
        transformations = [(0,1),(0,-1)]  
        return self._traverse(start_coords, colour, continuos, transformations, board)


    def _traverse_knight(self, start_coords, colour, board=False):
        board = self._check_board_given(board)
        transformations = [(1, 2) ,(-1, 2) ,(1, -2) ,(-1, -2) ,(2, 1) ,(-2, 1) ,(2, -1) ,(-2, -1)]
        moves = self._traverse(start_coords, colour, False, transformations, board)
        
        return moves


    def _traverse_pawn_vertical(self, start_coords, colour):
        transformations = self._get_pawn_vertical_transformations(start_coords, colour)
        moves = []
        for transformation in transformations:
            row, col = self.transform(start_coords, transformation)
            current = self.board[row][col]
            if current == '.':
                moves.append((row, col))
            else:
                break
        return moves


    def _traverse_pawn_diagonal(self, start_coords, colour, board=False):
        board = self._check_board_given(board)
        if colour == WHITE:
            transformations = [(-1,-1),(-1,1)]
        if colour == BLACK:
            transformations = [(1,-1),(1,1)]

        moves = []

        for transformation in transformations:
            row, col = self.transform(start_coords, transformation)
            if not self.is_on_board(row, col):
                continue
            coords = (row, col)
            current = board[row][col]
            en_passant = self.get_en_passant()
            if coords == en_passant:
                moves.append( coords )
            elif current == '.':
                continue
            elif self.code_to_colour(current) != colour:
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


    def _get_pawn_vertical_transformations(self, coords, colour):
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

        return transformations_vertical


    def _get_pawn_moves(self, coords, colour):
        moves = []
        moves += self._traverse_pawn_vertical(coords, colour)
        moves += self._traverse_pawn_diagonal(coords, colour)
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
        if not self._king_is_checked(coords, colour):
            moves += self._traverse_castling(colour)
        return moves


    # def winner(self):
    #     if self.red_left <= 0:
    #         return "GREEN WINS!"
    #     elif self.green_left <= 0:
    #         return "RED WINDS!"
    #     return None
