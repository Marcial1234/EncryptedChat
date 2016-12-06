#!/usr/bin/python
# test this line if you're in Mac/Linux

from dependencies import *
import os, sys, time #, socket
from socket import *

# pycrypto Package
# from Crypto.Cipher import AES
# I"m having issues having issues installing the AES package in UF's computers
# trying alternatives, like M2Crypto or open sourced vanilla AES implementations

# i wanted to use 65537/5 for something i think
all_threads = []

# Function for handling connections. This will be used to create threads
def clientthread(client):
    # Sending message to connected client
    client.send("Welcome to the server. Type something and hit enter\n") # send only takes string
    client.send("What's your name?\n") # send only takes string
    name = client.recv(1024)

    # infinite loop so that function and thread does not terminate
    while True:
        # Receiving from client
        data = client.recv(max_size)
        print name + " sent:\n" + data 
        client.sendall(data)
    
    client.close()

def main():
    # MAC Address code
    # from uuid import getnode as get_mac
    # addr = str(basic_key)
    # # this list comp formats the MAC Address from a Long to "XX:XX:.."
    # addr = ":".join(addr[i:i+2] for i in range(0,12,2))
    # # send server mac address to client as a test
    # client.send(addr)
    # basic_key = get_mac()
    
    host = "localhost"
    port =  52725 # Arbitrary port

    # instantiating server socket
    server = socket(AF_INET, SOCK_STREAM)
    print "Socket created"
    
    # Bind socket to local host and port
    # server.bind((host, port))

    # Debug Code
    try:
        server.bind((host, port))
    except error as msg:
        print "Bind failed. Error Code : " + str(msg[0]) + " Message " + msg[1]
        sys.exit()

    print "Socket bind complete"

    # Start listening on socket
    # Passed Parameter is # of max connections allowed
    server.listen(5)
    print "Socket now listening"

    # Stays Connected undefinately
    # still figuring out to how gracefully exit... (with Ctrl + C, or equivalent)
    while True:
        # Blocking code
        client, (ip,port) = server.accept()
        start_new_thread(clientthread, (client,))
        # now to send everyone's stuff
        print "Connected with " + ip + ":" + str(port)

    server.close()

if __name__ == "__main__":
    main()