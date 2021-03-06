#!/usr/bin/python

import os, sys, time, thread
from socket import *

# pycrypto Package
# from Crypto.Cipher import AES
# I"m having issues having issues installing the AES package in UF's computers
# trying alternatives, like M2Crypto or open sourced vanilla AES implementations

# i wanted to use 65537/5 for something i think
all_threads = []

# Function for handling connections. This will be used to create threads
def clientthread(client):
    all_threads.append(client)
    # Sending message to connected client
    client.send("Welcome to the server")
    client.send("What's your name?")
    name = client.recv(1024)

    # infinite loop so that function and thread does not terminate
    try:
        # prior, or something else. else it dies first hand
        data = " "
        while True:
            client.send("What's your message?")
            # Receiving from client
            data = client.recv(500)
            print name + " sent:\n" + data
            client.send(data)

            # so, now that we have this...
            # figure out multiple sockets

    except error:
        pass
    except KeyboardInterrupt:
        pass
    
    client.close()

def main():  
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
    server.listen(3)
    print "Socket now listening"

    # Stays Connected undefinately
    # still figuring out to how gracefully exit... (with Ctrl + C, or equivalent)
    try:
        while True:
            # Blocking code
            client, (ip,port) = server.accept()
            thread.start_new_thread(clientthread, (client,))
            # now to send everyone's stuff
            print "Connected with " + ip + ":" + str(port)
    except KeyboardInterrupt:
        pass

    print "\nGoodbye!"
    server.close()

if __name__ == "__main__":
    main()