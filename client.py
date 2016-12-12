#!/usr/bin/python

from random import randint, sample # PRNG
from Crypto.Cipher import AES
from Crypto import Random # Key generator
from socket import *
import os, sys, time

entropy = 23
# arbitrary prime number with generators

# Bases for generators of up to 23:
# [5, 7, 10, 11, 14, 15, 17, 19, 20, 21]
def get_offset(n, base=19):
    return int(base**n % entropy)

# Returns an 'n' sized string to be appened to ciphertext
def pad(n):
    # Explanation: this is a list comprehension.
    # The loop is ran, and each element inside is what is returned by what's before 'for'
    ## Code => padding 'n' [a-z, A-Z] characters to message
    return [chr(randint(0,25) + sample([65,97],1)[0]) for x in xrange(n)]

# Scrambles key and plaintext by the offset
# Returns: list of chars
def scramble(plaintext, key, offset):
    index = 0
    end = 16*offset
    ciphertext = []

    for index in xrange(0, end, offset):
        partition = plaintext[index:index+offset]
        ciphertext.extend(partition)
        ciphertext.extend(key[index/offset])

    ciphertext.extend(plaintext[(index-1)*(offset):])
    return ciphertext

# Unscrambles key and plaintext by the offset
# Returns: [list of chars, list of chars] => ciphertext, key
def unscramble(merged_ciphertext, offset):
    # Contraction
    m_c = merged_ciphertext
    end = (offset+1)*16+1
    ciphertext = []
    index = 0
    key = []

    while len(key) < 16 and index < end:
        ciphertext.extend(m_c[index:index+offset]) # lists slicing uses [) format
        key.append(m_c[index+offset])
        index += offset + 1

    ciphertext.extend(m_c[index+offset+1:])
    return [ciphertext, key]

#   Crypto part:
#       Encryption:
#           You create a one time AES key
#           You encrypt the Message using AES and the above key
#           Encrypted message is padded up to a certain number of characters (max length) with random text
#           You create a random character (a-w) that maps to 0-22 via ord([actual char]) - 97
#           You pass the random character thru one of the base generators for 23 (below) that returns the step value
#           You scramble the Key within the text in gaps of get_offset(random_char)
#           random_char goes in the front of the ciphertext
def encrypt(plaintext):
    # generate random_char
    random_int = randint(0,entropy-1)
    random_char = chr(random_int+97)
    offset = get_offset(random_int)

    # adding padding for spacing, and AES formatting
    needs = 16*offset - len(plaintext)
    if needs > 0:
        padding = pad(needs)
        plaintext += "".join(padding)
    
    # only pad the rest of the message if its length is not a multiple of 16
    needs = 16 - len(plaintext)%16
    if needs != 16:
        padding = pad(needs)
        plaintext += "".join(padding)
    
    # Generate Random Key, IV is just the reverse of the key
    key = Random.new().read(16)
    iv = key[::-1]

    # Using AES-128 CBC
    # source:
    # http://pythonhosted.org/pycrypto/Crypto.Cipher.AES-module.html#MODE_ECB
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = encryptor.encrypt(plaintext)

    # Scrambled Eggs time
    ciphertext = "".join([random_char] + scramble(ciphertext, key, offset))
    return ciphertext

# Decrypt:
# Delete first char, and pass it thru get_offset. 
# Use result to build key and message
def decrypt(message):
    # mapping random_char to (0-23) or (0-entropy/prime_number-1)
    random_int = ord(message[0]) - 97
    offset = get_offset(random_int)

    # skipping the random_int
    merged_ciphertext = message[1:] 

    # Unscramble
    ciphertext, key = unscramble(merged_ciphertext, offset)
    key = "".join(key)
    iv = key[::-1] # reseve of key
    ciphertext = "".join(ciphertext)

    # Decrypt, AES-128 CBC
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    plaintext = encryptor.decrypt(ciphertext)

    return plaintext

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
        message = encrypt(raw_input()) # Encrypt Message
        sock.send(message) # Send encrypted message
        data = sock.recv(750) # Receive Output from the server
        print "Decrypted message: \n" + decrypt(data) # Print decrypted message

    sock.close()

if __name__ == '__main__':
    main()