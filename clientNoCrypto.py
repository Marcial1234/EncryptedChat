#!/usr/bin/python

from socket import *
import os, sys, time


def main():
    host = 'localhost'
    port = 52725

    sock = socket()
    # Connecting to socket
    sock.connect((host, port))

    # Sending over Username
    print "server=> " + sock.recv(50) # Greetings
    print "server=> " + sock.recv(50) # Name Prompt
    sock.send(raw_input()) # Name Input

    # Infinite loop to keep client running
    while True:
        print "server=> " + sock.recv(50) # Message Prompt
        message = raw_input() # Get Message
        sock.send(message) # Send message
        data = sock.recv(750) # Receive Output from the server
        print data # Print  message

    sock.close()

if __name__ == '__main__':
    main()
