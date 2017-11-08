#code "help" took from stackoverflow.com
#Modules required.
#Tkinter
#pickle
#Tix

import random
import time
import Tkinter
import pickle
import socket
import sys
import os
from os import listdir
from os.path import isfile, join

from Tkinter import *
#from Tkinter.constants import *
from Tix import FileSelectBox, Tk


random.seed(time.time())



# There are probably a few bugs in this class, and it could be implemented
# better I think.
class SudokuBoard:
    """
    Data structure representing the board of a Sudoku game.
    """
    def __init__(self):
        self.clear()

    def clear(self):
        #empty the board
        self.grid = [[0 for x in range(9)] for y in range(9)]
        self.locked = []

    def get_row(self, row):
        return self.grid[row]

    def get_cols(self, col):
        return [y[col] for y in self.grid]

    def get_nearest_region(self, col, row):
        """
        Regions are 3x3 sections of the grid.
        """
        def make_index(v):
            if v <= 2:
                return 0
            elif v <= 5:
                return 3
            else:
                return 6
        return [y[make_index(col):make_index(col)+3] for y in
                self.grid[make_index(row):make_index(row)+3]]

    def set(self, col, row, v, lock=False):
        if v == self.grid[row][col] or (col, row) in self.locked:
            return
        for v2 in self.get_row(row):
            if v == v2:
                raise ValueError()
        for v2 in self.get_cols(col):
            if v == v2:
                raise ValueError()
        for y in self.get_nearest_region(col, row):
            for x in y:
                if v == x:
                    raise ValueError()
        self.grid[row][col] = v
        if lock:
            self.locked.append((col, row))

    def get(self, col, row):
        return self.grid[row][col]

    def __str__(self):
        strings = []
        newline_counter = 0
        for y in self.grid:
                strings.append("%d%d%d %d%d%d %d%d%d" % tuple(y))
                newline_counter += 1
                if newline_counter == 3:
                    strings.append('')
                    newline_counter = 0
        return '\n'.join(strings)

def sudogen_1(board):
    """
    Algorithm:
        Add a random number between 1-9 to each subgrid in the
        board, do not add duplicate random numbers.
    """
    board.clear()
    added = [0]
    for y in range(0, 9, 3):
        for x in range(0, 9, 3):
            if len(added) == 10:
                return
            i = 0
            while i in added:
                i = random.randint(1, 9)
            try:
                board.set(random.randint(x, x+2), random.randint(y, y+2), i, lock=True)
            except ValueError:
                print("Board rule violation, this shouldn't happen!")
            added.append(i)

def rgb(red, green, blue):
    """
    Make a Tkinter compatible RGB color.
    """
    return "#%02x%02x%02x" % (red, green, blue)

class SudokuGUI(Frame):
    board_generators = {"SudoGen v1 (Very Easy)":sudogen_1}
    board_generator = staticmethod(sudogen_1)

    def new_game(self):
        self.board.clear()
        self.board_generator(self.board)
        self.sync_board_and_canvas()

    def make_modal_window(self, title):
        window = Toplevel()
        window.title(title)
        window.attributes('-topmost', True)
        window.grab_set()
        window.focus_force()
        return window



    def make_grid(self):
        c = Canvas(self, bg=rgb(128,128,128), width='512', height='512')
        c.pack(side='top', fill='both', expand='1')

        self.rects = [[None for x in range(9)] for y in range(9)]
        self.handles = [[None for x in range(9)] for y in range(9)]
        rsize = 512/9
        guidesize = 512/3

        for y in range(9):
            for x in range(9):
                (xr, yr) = (x*guidesize, y*guidesize)
                self.rects[y][x] = c.create_rectangle(xr, yr, xr+guidesize,
                                                      yr+guidesize, width=3)
                (xr, yr) = (x*rsize, y*rsize)
                r = c.create_rectangle(xr, yr, xr+rsize, yr+rsize)
                t = c.create_text(xr+rsize/2, yr+rsize/2, text="SUDO",
                                  font="System 15 bold")
                self.handles[y][x] = (r, t)

        self.canvas = c
        self.sync_board_and_canvas()

    def sync_board_and_canvas(self):
        g = self.board.grid
        for y in range(9):
            for x in range(9):
                if g[y][x] != 0:
                    self.canvas.itemconfig(self.handles[y][x][1],
                                           text=str(g[y][x]))
                else:
                    self.canvas.itemconfig(self.handles[y][x][1],
                                           text='')

    def canvas_click(self, event):
        print("Click! (%d,%d)" % (event.x, event.y))
        self.canvas.focus_set()
        rsize = 512/9
        (x,y) = (0, 0)
        if event.x > rsize:
            x = int(event.x/rsize)
        if event.y > rsize:
            y = int(event.y/rsize)
        print(x,y)
        if self.current:
            (tx, ty) = self.current
            #self.canvas.itemconfig(self.handles[ty][tx][0], fill=rgb(128,128,128))
        self.current = (x,y)

        # BUG: Changing the color of the background of a tile erases parts of
        #      the thick gridlines
        #self.canvas.itemconfig(self.handles[y][x][0], fill=rgb(255,255,255))

    def canvas_key(self, event):
        print("Clack! (%s)" % (event.char))
        socket1.send(event.char)
        response=socket1.recv(1024)
        (x,y) = self.current
        try:
            self.board.set(x, y, int(response))
            self.sync_board_and_canvas()
        except ValueError:
            print("Value is not allowed but score deduced.")
            pass

    def __init__(self, master, board):


        Frame.__init__(self, master)

        if master:
            master.title("Sudoku GUI")

        self.board = board
        self.board_generator(board)
        bframe = Frame(self)

        #generate new random board.
        self.ng = Button(bframe, command=self.new_game, text="New Game")
        self.ng.pack(side='left', fill='x', expand='1')


        bframe.pack(side='bottom', fill='x', expand='1')
        self.make_grid()
        self.canvas.bind("<Button-1>", self.canvas_click)
        self.canvas.bind("<Key>", self.canvas_key)

        self.current = None
        self.pack()

if __name__ == '__main__':

    HOST = 'localhost'  # server name goes in here
    PORT = 32788

    socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket1.connect((HOST, PORT))

    board = SudokuBoard()
    tk = Tk()
    gui = SudokuGUI(tk, board)
    gui.mainloop()
