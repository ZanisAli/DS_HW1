import socket
import threading


#  To Send a random number between 1-9 to each Clients
def Gen_send_sukodu_Random_9Numbers():
    Data='102232371415544665717837978'
    print "The Random Generated Numbers have sent to the Cliens  ", Data
    send_data(str(Data))

connections = set()
# To send processed data to the Clients
def send_data(message):
    for connection in connections:
        print "Sending %s" % message
        connection.send(str(message))

# To receive data from clients
def receive_data(connection):
    nicknameofplayers = ''
    while True:
        print "Waiting for message"

        message = connection.recv(1024)
        if((len(message)>4 and len(message)<9)):
            nicknameofplayers = message
            nicknameslist(nicknameofplayers,address)
        else:

            if not message:
                print "Closing connection and removing from registry"
                connections.remove(connection)
                return
            print "Received %s, sending to all" % message, address
        send_data(message)

#Server Buffer to save the nicknames and address of clients
list = []


def nicknameslist(nick,address):
    global list
    list.append(nick)
    list.append(address)
    print "The Buffer of Server has a client ===>>>> :",list
    print "Clients are are now connected....  ===>>> :",list










# Set up the listening socket
sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sckt.bind(('127.0.0.1', 9999))
sckt.listen(10)

# The connections should be in a loop
while True:
    print "Waiting for a connection"
    (connection, address) = sckt.accept()
    print "Connection received. Adding to registry"
    print "The Client", address, "is now connected..."
    connections.add(connection)
    threading.Thread(target = receive_data, args=[connection]).start()
    Gen_send_sukodu_Random_9Numbers()