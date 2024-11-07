from .constants import SQUARE_SIZE, PIECE_SPRITES, CODE_TO_NAME, BLACK, WHITE


class Piece:


    def __init__(self, row, col, piece):
        self.row = row
        self.col = col
        self.piece_code = piece
        self.piece_type = CODE_TO_NAME[piece.lower()]
        if piece.lower() == piece:
            self.colour = BLACK
        else:
            self.colour = WHITE
        self.piece_sprite = self.get_sprite(piece)
        self.x = 0
        self.y = 0
        self.calc_pos()


    def get_piece_code(self):
        return self.piece_code


    def get_piece_type(self):
        return self.piece_type


    def get_coords(self):
        return (self.x, self.y)


    def get_sprite(self,piece):
        try:
            sprite = PIECE_SPRITES[piece]
            return sprite
        except KeyError:
            print('STOP there that piece does not exist')
            return False


    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2


    def get_pos(self):
        return (self.row, self.col)


    def get_colour(self):
        return self.colour


    def get_colour_full(self):
        if self.colour == WHITE:
            return 'WHITE'
        else:
            return 'BLACK'


    def draw(self, win):
        PIECE = self.piece_sprite
        win.blit(PIECE, (self.x - PIECE.get_width()//2, self.y - PIECE.get_height()//2))


    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()


    def __repr__(self):
        return self.piece_code


    def __str__(self):
        output = 'Colour = ' + self.get_colour_full() + '\n'
        output += 'Code = ' + self.get_piece_code() + '\n'
        output += 'Type = ' + self.get_piece_type() + '\n'
        output += '(row, col) = ' + str(self.get_pos()) + '\n'
        output += '(x, y) = ' + str(self.get_coords()) + '\n'
        return output

