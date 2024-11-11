from tkinter import *

class EvolvePawn:
    def __init__(self, output):
        self.root = Tk()
        self.root.eval('tk::PlaceWindow . center')
        self.output = output
        self.root.title("Evolve Pawn")
        self.root.geometry('200x120')
        lbl = Label(self.root, text = "Evolve pawn into:")
        lbl.grid(column=0, row=0)
        btn_queen = Button(self.root, text = "Queen" ,
                    fg = "black", command=self.queen, height=2, width=6)
        btn_bishop = Button(self.root, text = "Bishop" ,
                    fg = "black", command=self.bishop, height=2, width=6)
        btn_rook = Button(self.root, text = "Rook " ,
                    fg = "black", command=self.rook, height=2, width=6)
        btn_knight = Button(self.root, text = "Knight" ,
                    fg = "black", command=self.knight, height=2, width=6)
        btn_queen.grid(column=0, row=1)
        btn_bishop.grid(column=1, row=1)
        btn_rook.grid(column=0, row=2)
        btn_knight.grid(column=1, row=2)
        self.root.mainloop()

    def queen(self):
        self.output.append('q')
        self.root.destroy()


    def bishop(self):
        self.output.append('b')
        self.root.destroy()


    def rook(self):
        self.output.append('r')
        self.root.destroy()


    def knight(self):
        self.output.append('n')
        self.root.destroy()