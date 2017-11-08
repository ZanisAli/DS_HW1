import socket
import sys
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
HOST = 'localhost'
PORT = 32788


socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((HOST, PORT))

socket.listen(1)

def check(rec):
    if rec.isdigit() and int(rec) >0 :
        conn.send(rec)
    else:
        print("Value is not allowed but score deduced.")




while (1):

    conn, addr = socket.accept()
    print 'New client connected ..'
    while(True):
        rec=conn.recv(1024)
        print(rec)
        check(rec)

    conn.close()
