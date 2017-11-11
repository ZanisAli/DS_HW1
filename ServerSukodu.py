
import random
import time
import os
#import tkinter.tix
import pickle
from Tkinter import *
#from Tkinter.constants import *
#from Tkinter.tix import FileSelectBox, Tk
import socket
import threading


def Gen_send_sukodu_Random_9Numbers():
    """
    Algorithm:
        Add a random number between 1-9 to each subgrid in the
        board, do not add duplicate random numbers.
    """
    Data='912837645567894321321457698'
    print "stringgggggggggggggggggggggggggggg", Data
    send_all(str(Data))


def check(rec):
    if rec.isdigit() and int(rec) >0 :
        connection.send(rec)
    else:
        print("Value not allowed, score deduced")
        sys.exit()




connections = set()

# Function to send processed data to the Clients
def send_all(message):
    for connection in connections:
        print "Sending %s" % message
        connection.send(message)

# Function to receive data from clients
def receive(connection):
    while True:
        print "Waiting for message"
        message = connection.recv(1024)
        if not message:
            print "Closing connection and removing from registry"
            connections.remove(connection)
            return
        print "Received %s, sending to all" % message
        send_all(message)



# Set up the listening socket
sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sckt.bind(('127.0.0.1', 9999))
sckt.listen(10)

# We must accept connections in a loop
while True:
    print "Waiting for a connection"

    (connection, address) = sckt.accept()

    print "Connection received. Adding to registry"
    connections.add(connection)

    print "Spawning receiver"
    threading.Thread(target = receive, args=[connection]).start()
   # print "77777777777777777777", threading.current_thread()
    Gen_send_sukodu_Random_9Numbers()