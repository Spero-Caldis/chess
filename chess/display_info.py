import pygame

class DisplayInfo:
    def __init__(self, surface, turn, halfmove, fullmove):
        self.win = surface
        self.turn = turn
        self.halfmove = halfmove
        self.fullmove = fullmove