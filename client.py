#!/usr/bin/python

from random import randint, sample # PRNG
from Crypto.Cipher import AES
from dependencies import * # common variables, so far not worth it but w/e
from Crypto import Random # Key generator
from socket import *
# from math import ceil
import os, sys, time

entropy = 23
# above*len(key) 23*16
set_size = 368
# arbitrary

# Bases for generators of up to 23:
# [5, 7, 10, 11, 14, 15, 17, 19, 20, 21]
def get_offset(n, base=19):
    return int(base**n % entropy)

# Returns an 'n' sized string to be appened to ciphertext
def pad(n):
    # Explanation: this is a list comprehension.
    # The loop is ran, and each element inside is what is returned by what's before 'for'
    ## Code => padding can be upper and lower case
    return [chr(randint(0,22) + sample([64,96],1)[0]) for x in xrange(n)]

# Scrambles key and plaintext by the offset
# Returns: list of chars
def scramble(plaintext, key, offset):
    index = 0
    ciphertext = []
    for index in xrange(0, len(plaintext), offset):
        partition = plaintext[index:index+offset]
        ciphertext.extend(partition)
        ciphertext.extend(key[index/offset])
        ## Debug Code
        # print index, index+offset, oink
        # print key[index/offset]

    ciphertext.extend(plaintext[index*(offset+1):])
    return ciphertext

# Unscrambles key and plaintext by the offset
# Returns: [list of chars, list of chars] => ciphertext, key
def unscramble(merged_ciphertext, offset):
    # Contraction
    m_c = merged_ciphertext
    end = len(m_c)-offset+1
    ciphertext = []
    index = 0
    key = []

    for index in xrange(0, end, offset+1):
        ciphertext.extend(m_c[index:index+offset]) # lists slicing uses [) format
        key.append(m_c[index+offset])
        ## Debug Code
        # print index, index+offset, m_c[index:index+offset], m_c[index+offset]

    ciphertext.extend(m_c[index+offset+1:])
    return [ciphertext, key]

#   Crypto part:
#       Encryption:
#           You create a one time AES key
#           You encrypt the Message using AES and the above key
#           Encrypted message is padded up to a certain number of characters (max length) with random text
#           You create a random character (a-z, {|}~) that maps to 0-28 via ord([actual char]) - 97
#           You pass the random character thru one of the base generators for 29 (below) that returns the step value
#           You scramble the Key within the text in gaps of get_offset(random_char)
#           random_char goes in the front of the ciphertext
def encrypt(plaintext):
    # generate random char
    random_int = randint(0,22)
    random_char = chr(random_int+97)
    offset = get_offset(random_int)

    # need to pad with all 0s? you can go for it
    needs = 16 - len(plaintext)%16
    plaintext = plaintext.split()
    plaintext.extend(pad(needs))
    plaintext = "".join(plaintext)
    
    # Generate Random Key, IV is just the reverse
    key = Random.new().read(16)
    iv = key[::-1]

    # Using AES-128 CBC (Cipher-Block Chaining)
    # http://pythonhosted.org/pycrypto/Crypto.Cipher.AES-module.html#MODE_ECB
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = encryptor.encrypt(plaintext)

    # getting rid of "="
    ciphertext = [char for char in ciphertext if char != "="]

    # Add Random Padding for up to the next Block
    needs = offset*16-len(ciphertext)
    ciphertext.extend(pad(needs))

    # Scrambled Eggs time
    ciphertext = "".join([random_char] + scramble(ciphertext, key, offset))
    # ciphertext = [random_char] + ciphertext

    return ciphertext

# Decrypt:
# Delete first char, and pass it thru get_offset. 
# Use result to build key and message
def decrypt(message):
    if len(message) == 0:
        return ""

    random_int = ord(message[0]) - 97
    offset = get_offset(random_int)

    # skipping the random_int
    merged_ciphertext = message[1:] 

    # Unscramble
    ciphertext, key = unscramble(merged_ciphertext, offset)
    key = "".join(key)
    ciphertext = "".join(ciphertext)


    # Decrypt, AES-128 CBC
    encryptor = AES.new(key, AES.MODE_CBC, key[::-1])
    plaintext = encryptor.encrypt(ciphertext)

    return plaintext

# Client code talking to server:
# https://neerajkhandelwal.wordpress.com/2012/02/16/socket-programming-handling-multiclients/
def main():
    host = 'localhost'
    port = 52725
    # port = 52000
    # port = 65535/7
     
    sock = socket()
    # Connecting to socket
    sock.connect((host, port))
     
    # Sending over Username
    print sock.recv(50) # Greetings
    print sock.recv(50) # Name?
    sock.send(raw_input()) # Name

    # Infinite loop to keep client running.
    while True:
        print sock.recv(50) # Message?
        message = encrypt(raw_input())
        sock.send()

        data = sock.recv(max_size*2)
        # wait for next if message received it's not the specific length
        if len(data) > max_size or data == message:
            sock.recv(50)
            continue
            # sock.send(encrypt(raw_input()))

        print decrypt(data)

    # try:
    #   print raw_input()
    # except KeyboardInterrupt:
    #   print "oink"

    sock.close()

if __name__ == '__main__':
    main()