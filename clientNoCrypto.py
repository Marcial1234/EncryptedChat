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
    print sock.recv(50) # Greetings
    print "server=> " + sock.recv(50) # Name?
    sock.send(raw_input()) # Name

    # Infinite loop to keep client running.
    while True:
        print "server=> " + sock.recv(50) # Message?
        sock.send(raw_input())
        data = sock.recv(750)
        print "server=> " + data

    sock.close()

if __name__ == '__main__':
    main()
