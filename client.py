#!/usr/bin/python
import os, sys, socket, time
from random import randint
from socket import *

# Bases for generators of up to 29:
# 2, 3, 8, 10, 11, 14, 15, 18, 19, 21, 26, 27
# Up to 23:
# 5, 7, 10, 11, 14, 15, 17, 19, 20, 21,
def get_offset(n, base=19):
    return base**n % base

# returns an 'n' sized string to be appened to plaintext
def pad(n):
    # Explination: this is a list comprehension.
    # The loop is ran, and each element inside is what is returned by what's before 'for'
    return [chr(randint(0,28)+97) for x in xrange(n)]

# Scrambles key and plaintext by the offset
# Returns: list of chars
def scramble(plaintext, key, offset):
    ciphertext = []
    for index in xrange(0, len(plaintext), offset):
        partition = plaintext[index:index+offset]
        ciphertext.extend(partition)
        ciphertext.extend(key[index/offset])
        # Debug Code
        # print index, index+offset, oink
        # print key[index/offset]
    # Index still on the scope
    ciphertext.extend(plaintext[index*(offset+1):])
    return ciphertext

# Unscrambles key and plaintext by the offset
# Returns: [list of chars, list of chars]
def unscramble(ciphertext, offset):
    plaintext = []
    key = []

    for index in xrange(0, len(ciphertext)-offset+1, offset+1):
        plaintext.extend(message[index:index+offset])
        key.append(message[index+offset])
        # Debug Code
        # print index, index+offset, message[index:index+offset], message[index+offset]

    # Index still on the scope
    plaintext.extend(message[index+offset+1:])
    [plaintext, key]

#   Crypto part:
#       Encryption:
#           Message is padded up to a certain number of characters (max length) with random text
#           You create a one time AES key
#           You encrypt the Message using AES and the above key
#           You create a random character (a-z, {|}~) that maps to 0-28 via ord([actual char]) - 97
#           You pass the random character thru one of the base generators for 29 (below) that return the step/increment value
#           You scramble the Key within the text in gaps of getoffset(randchar)
#           randchar goes in the front of the ciphertext
def encrypt(message):
    # messagee is turned into a list
    plaintext = message.split()
    ciphertext = []

    # Add Random Padding
    # set_size NOT SET, just placeholder
    plaintext.extend(pad(set_size-len(plaintext)))

    # this turns plaintext into a string
    # plaintext = "".join(plaintext)

    # everything below doesn't work yet, just a placeholder
    key = AES.generate_key(128)
    # Scrambled Eggs Time
    cyphertext = "".join(scramble(plaintext, key, offset))
    output = AES.encrypt(cyphertext, key)
    return output

# Decrypt:
# Delete first char, and pass it thru getoffset. Use result to build key and message
# AES Decrypt
def decrypt(message):
    # if the message received it's not the specific size/length, return and print nothing
    if len(message) != size:
        return ""
    # IS IT QUARANTEED THAT THIS WILL HAPPEN ALL THE TIME??
    # NEED TO TEST AES RETURN SIZE GIVEN MANY INPUTS

    # DO THE THING
    random_char = ord(message[0]) - 97
    offset = get_offset(random_char)

    # skipping the random_char
    merged_ciphertext = message[1:] 
    # will be turned into strings later

    # Unscramble, not done
    plaintext, key = unscramble(merged_ciphertext, offset)

    # this doesn't work yet, just a placeholder
    plaintext = AES.decrypt(cyphertext, key)
    return plaintext

# Client code talking to server:
# https://neerajkhandelwal.wordpress.com/2012/02/16/socket-programming-handling-multiclients/
def main():
    host = 'localhost' # '127.0.0.1' can also be used
    # port = 52000
    port = 52725
    # port = 65535/7
     
    sock = socket()
    # Connecting to socket
    sock.connect((host, port)) # Connect takes tuple of host and port
     
    # Infinite loop to keep client running.
    while True:
        data = sock.recv(1024)
        print data
        sock.send('HI! I am client.')
     
    sock.close()

if __name__ == '__main__':
    main()