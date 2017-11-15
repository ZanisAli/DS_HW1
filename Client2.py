import socket
import threading
import select
import random
import time
import winsound
import winsound as wav
import tkMessageBox
import Tkinter
from Tkinter import *
import tkMessageBox
import Queue
from easygui import *

exiting = False
random.seed(time.time())

# Initialise a global variables
coun2 = 0
increment = 0


# This is Class to organise the data in main grid ( 9 columns, 9 rows), and 9 subgrids (3 column, 3 rows)
class SudokuBoard:
    def __init__(self):
        self.clear()

    # To clear the grid
    def clear(self):
        self.grid = [[0 for x in range(9)] for y in range(9)]
        self.locked = []

    # To get the numbers from rows
    def get_row(self, row):
        return self.grid[row]

    # To get the numbers from columns
    def get_cols(self, col):
        return [y[col] for y in self.grid]

    # To get numbers from the subgrids
    def get_nearest_region(self, col, row):

        def make_index(v):
            if v <= 2:
                return 0
            elif v <= 5:
                return 3
            else:
                return 6

        return [y[make_index(col):make_index(col) + 3] for y in
                self.grid[make_index(row):make_index(row) + 3]]

    # To set the numbers into the subgrids
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


# Function to receive processed data from server
Checker = '1020'


def recv_loop(connection):
    global Randomnumber
    global Checker
    global increment
    global nickname2

    while True:
        if exiting:
            print "Ending receive loop"
            return
        (readable, writable, errored) = select.select([connection], [], [connection], 0.1)
        if readable or errored:

            message = connection.recv(1024)
            if not message:
                print "Disconnected"
                return
            if (len(message) == 27):
                Randomnumber = message
                print "Insied recv loop, Length of Message is =", len(message), "The Message is =", message
            elif (len(message) == 4):
                Checker = message
                recivepacket(board)
            elif ((len(message) > 4 and len(message) < 9)):
                nickname2 = message
            else:
                increment = message


def packetchhecker():
    string1 = Checker
    return string1


def sudogen_1(board):
    global coun2
    """
    Algorithm:
        Add a random number between 1-9 to each subgrid in the
        board, That numbers transmitted from server to the clients at the same time and same positions
    """
    pq = Randomnumber
    added = [0]
    print"Main Numbers in Canvas =", pq
    for n in range(0, 26, 3):
        i = int(pq[n])
        x = int(pq[n + 1])
        y = int(pq[n + 2])
        print "Number is :", i, "(X=", x, ",", "Y=", y, ")"
        try:
            board.set(x, y, i, lock=True)
        except ValueError:
            print("Some problem occurred in board, this shouldn't happen!")


# To Receive the data packet from another clients via through server
# Data packet consists of the number (ir) and the position of the number in grid (xr,xy)
def recivepacket(board):
    PacketToRecive = packetchhecker()
    wav.PlaySound("beep.wav", wav.SND_ASYNC)
    print"Packet of Data Transmitted from Client 2 is = ", PacketToRecive
    countplayer2 = +1
    ir = int(PacketToRecive[0])
    xr = int(PacketToRecive[1])
    yr = int(PacketToRecive[2])
    board.set(xr, yr, ir, lock=True)


def rgb(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)


class SudokuGUI(Frame):
    board_generators = {"SudoGen v1 (Very Easy)": sudogen_1}
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

    def query_board(self):
        window = self.make_modal_window("Set Board Algorithm")

        scroll = Scrollbar(window)
        scroll.pack(side='right', fill='y')

        listbox = Listbox(window, yscrollcommand=scroll.set)

        scroll.config(command=listbox.yview)

        bframe = Frame(window)

        for s in self.board_generators.keys():
            listbox.insert(-1, s)

        def do_ok():
            self.board_generator = self.board_generators[listbox.get(ACTIVE)]
            window.destroy()

        def do_cancel():
            window.destroy()

        ok = Button(bframe, command=do_ok, text="Ok")
        ok.pack(side='right', fill='x')

        listbox.pack(side='top', fill='both', expand='1')
        bframe.pack(side='top', fill='x', expand='1')

        window.mainloop()

    def make_grid(self):
        global coun1

        c = Canvas(self, bg=rgb(68, 90, 235), width='512', height='512')

        ###################################### Labels TO initilaize Players
        widget = Label(c, text='Player 1', fg='yellow', bg='black')
        widget.pack()
        c.create_window(575, 35, window=widget)
        c.pack(side='top', fill='both', expand='5')

        widget = Label(c, text='Player 2', fg='yellow', bg='black')
        widget.pack()
        c.create_window(575, 200, window=widget)
        c.pack(side='top', fill='both', expand='5')

        ################################# Labels For Naick Names of Players
        widget = Label(c, text='Nickname', fg='yellow', bg='black')
        widget.pack()
        c.create_window(575, 60, window=widget)
        c.pack(side='top', fill='both', expand='10')

        widget = Label(c, text='Nickname', fg='yellow', bg='black')
        widget.pack()
        c.create_window(575, 225, window=widget)
        c.pack(side='top', fill='both', expand='5')

        self.rects = [[None for x in range(9)] for y in range(9)]
        self.handles = [[None for x in range(9)] for y in range(9)]
        rsize = 512 / 9
        guidesize = 512 / 3
        Label(tk,
              text=" Sudoku Game",
              fg="blue",
              font="Verdana 10 bold").pack()
        Label(tk,
              text="Institute of Computer Science, University of Trtu",
              fg="blue",
              font="Verdana 10 bold").pack()

        for y in range(9):
            for x in range(9):
                (xr, yr) = (x * guidesize, y * guidesize)
                self.rects[y][x] = c.create_rectangle(xr, yr, xr + guidesize,
                                                      yr + guidesize, width=10, )
                (xr, yr) = (x * rsize, y * rsize)
                r = c.create_rectangle(xr, yr, xr + rsize, yr + rsize)
                t = c.create_text(xr + rsize / 2, yr + rsize / 2, text="TIME",
                                  font="System 15 bold")
                self.handles[y][x] = (r, t)

        self.canvas = c
        self.sync_board_and_canvas()

    #################################################################################################
    def sync_board_and_canvas(self):
        g = self.board.grid
        for y in range(9):
            for x in range(9):
                if g[y][x] != 0:
                    self.canvas.itemconfig(self.handles[y][x][1], text=str(g[y][x]))
                    Counter1 = +1
                else:
                    self.canvas.itemconfig(self.handles[y][x][1], text='')

        return Counter1

    ##################################################################################################

    def canvas_click(self, event):

        print("Click! (%d,%d)" % (event.x, event.y))
        self.canvas.focus_set()
        rsize = 512 / 9
        (x, y) = (0, 0)
        if event.x > rsize:
            x = int(event.x / rsize)
        if event.y > rsize:
            y = int(event.y / rsize)
        print(x, y)
        if self.current:
            (tx, ty) = self.current
        self.current = (x, y)

    def canvas_key(self, event):
        PacketToSend = ''
        global coun2
        global nickname2
        nickm2 = nickname2
        global increment
        coun1 = increment
        print("Clack! (%s)" % (event.char))
        if event.char.isdigit() and int(event.char) > 0 and self.current:
            (xs, ys) = self.current
        try:
            self.board.set(xs, ys, int(event.char))
            self.sync_board_and_canvas()
            cs = self.sync_board_and_canvas()
            coun2 += 1
            PacketToSend = str(int(event.char))
            PacketToSend += str(xs)
            PacketToSend += str(ys)
            PacketToSend += str(cs)

            event.time
            sckt.send(PacketToSend)
            wav.PlaySound("beep.wav", wav.SND_ASYNC)
        except ValueError:
            tkMessageBox.showerror("Denied", "Wrong Input,  Your Score   -1     ")
            coun2 = coun2 - 1
            pass
        print"The Scores Of Player2 (", value2, ")  is  = ", coun2
        print"The Scores Of Player1  (", nickm2, ")  is  = ", coun1
        PacketToSend = ''
        sckt.send(str(coun2))

    def __init__(self, master, board):
        Frame.__init__(self, master)

        if master:
            master.title("Player 2")
        self.board = board
        self.board_generator(board)
        bframe = Frame(self)
        self.ng = Button(bframe, command=self.new_game, text="New Game")
        self.ng.pack(side='left', fill='x', expand='1')

        self.query = Button(bframe, command=self.query_board, text="Exit")
        self.query.pack(side='left', fill='x', expand='1')

        bframe.pack(side='bottom', fill='x', expand='1')
        self.make_grid()
        self.canvas.bind("<Button-1>", self.canvas_click)
        self.canvas.bind("<Key>", self.canvas_key)
        self.current = None
        self.pack()


# Connect the client with server
sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('127.0.0.1', 9999)
print "Connecting to server"
sckt.connect(('127.0.0.1', 9999))

# Receive Thread
print "Starting receive thread"
threading.Thread(target=recv_loop, args=[sckt]).start()

if __name__ == '__main__':
    while (True):
        value2 = enterbox("   Please Enter Your Nickname", " Welcome To Sukodu")
        if ((len(value2) > 8 or len(value2) < 5) or (value2 == '') or (value2.isspace())):
            msgbox("Your Nickname should be in between 4 to 8 length, Please Try Again......", " Wrong Input")
        else:
            msgbox("                          You Are Welcome  :" + str(value2), "Session has started")
            tk = Tk()
            board = SudokuBoard()
            gui = SudokuGUI(tk, board)
            sckt.send(value2)
            gui.mainloop()

while True:
    message = raw_input('>')
    if message == 'exit':
        exiting = True
        break
    sckt.send(message)


