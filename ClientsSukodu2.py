#Soduku GUI code help taken from stackoverflow.com
import socket
import threading
import select
import random
import time
from Tkinter import *
import Queue



exiting = False
random.seed(time.time())





RGN = '= no data'


class SudokuBoard:
    """
    Data structure representing the board of a Sudoku game.
    """
    def __init__(self):
        self.clear()

    def clear(self):
        """
        Empty the board.
        """
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

newone=''
# Function to receive processed data from server
def recv_loop( connection):
    outstring=''
    global Randomnumber
    global Checker
    global increment
    outstring = ''

    while True:

        if exiting:
            print "Ending receive loop"
            return
        (readable, writable, errored) = select.select([connection], [], [connection], 0.1)
        if readable or errored:
            message = connection.recv(1024)
            Randomnumber=message




            if not message:
                print "Disconnected"
                return
            print "insied recv lopprrrrrrrrrrrrrrrrrrrrr", message
            outstring=outstring+message
            Checker=outstring
            if(len(Checker)>3):
                pass
            else:
                slicing()
            outstring=''
def slicing():
    global newone
    toslice=Checker
    print("slicing function received ", toslice)
    newone=newone+toslice
    print("final",newone)
    print ("length",len(newone))
    if (len(newone)<3):
        pass
    else:
        try:
            x=int(newone[0])
            y=int(newone[1])
            i=int(newone[2])
            print("numbers =",x,y,i)
            board.set(x, y, i, lock=True)
            newone=''
        except ValueError:
            print ("not setting to board.")




           # board.set(int(message), int(message), int(message))





#def setstartgame(message):

 # global RGN
  #RNG=message
  #print "message ins side the function =",message


def sudogen_1(board):
    """
    Algorithm:
        Add a random number between 1-9 to each subgrid in the
        board, do not add duplicate random numbers.
    """
    pq=Randomnumber
    print"42342342343",pq
    added = [0]
    print"GRNNNNNNNNNN=", pq
    for n in range(1,9):

        x = int(pq[n])
        y = int(pq[n + 1])
        i = int(pq[n + 2])

        print "xxxxxx=", x, "yyyy=", y, "iiiii=", i
        try:
          board.set(x, y, i, lock=True)
        except ValueError:
            print("Board rule violation, this shouldn't happen!")




def rgb(red, green, blue):
    """
    Make a tkinter compatible RGB color.
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


        cancel = Button(bframe, command=do_cancel, text="Cancel")
        cancel.pack(side='right', fill='x')

        ok = Button(bframe, command=do_ok, text="Ok")
        ok.pack(side='right', fill='x')

        listbox.pack(side='top', fill='both', expand='1')
        bframe.pack(side='top', fill='x', expand='1')

        window.mainloop()

    def make_grid(self):
        c = Canvas(self, bg=rgb(128,128,52), width='640', height='512')
        c.pack(side='top', fill='both', expand='5')

        self.rects = [[None for x in range(9)] for y in range(9)]
        self.handles = [[None for x in range(9)] for y in range(9)]
        rsize = 512/9
        guidesize = 512/3
        Label(tk,
              text=" Sudoku Solver",
              fg="blue",
              font="Times").pack()

        w = Label(tk,
                  justify=RIGHT,
                  compound=RIGHT,
                  padx=25,
                  ).pack(side="left")

        w = Label(tk,
                  justify=LEFT,
                  compound=LEFT,
                  padx=25,
                  ).pack(side="right")

        for y in range(9):
            for x in range(9):
                (xr, yr) = (x*guidesize, y*guidesize)
                self.rects[y][x] = c.create_rectangle(xr, yr, xr+guidesize,
                                                      yr+guidesize, width=10,)
                (xr, yr) = (x*rsize, y*rsize)
                r = c.create_rectangle(xr, yr, xr+rsize, yr+rsize)
                t = c.create_text(xr+rsize/2, yr+rsize/2, text="SUDO",
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
                    self.canvas.itemconfig(self.handles[y][x][1],text=str(g[y][x]))
                else:
                    self.canvas.itemconfig(self.handles[y][x][1],text='')
##################################################################################################
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
        self.current = (x,y)

    def canvas_key(self, event):
        print("Clack! (%s)" % (event.char))
        sckt.send(event.char)
        response=sckt.recv(1024)
        (x,y) = self.current

        string1=str(x)
        string2=str(y)
        sckt.send(string1)
        sckt.send(string2)
        str1res=sckt.recv(1024)
        str2res=sckt.recv(1024)
        p=int(str1res)
        q=int(str2res)
        print("p",p)
        print("q",q)
        try:
            self.board.set(p, q, int(response))
            self.sync_board_and_canvas()
        except ValueError:
            print("Value is not allowed but score deduced.")
            pass




    def __init__(self, master, board):
        Frame.__init__(self, master)

        if master:
            master.title("Player 2")
        self.board = board
        self.board_generator(board)
        bframe = Frame(self)
        self.ng = Button(bframe, command=self.new_game, text="New Game")
        self.ng.pack(side='left', fill='x', expand='1')

        self.query = Button(bframe, command=self.query_board, text="Set Board Algorithm")
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




  #  time.sleep(10)
print "Starting receive thread"

threading.Thread(target=recv_loop, args=[sckt]).start()
print "77777777777777777777",threading.current_thread()
if __name__ == '__main__':


    board = SudokuBoard()

    tk = Tk()
    gui = SudokuGUI(tk, board)
    gui.mainloop()

while True:
    message = raw_input('>')
    if message == 'exit':
        exiting = True
        break
    sckt.send(message)

