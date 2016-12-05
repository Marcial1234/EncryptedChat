#!/usr/bin/python
import os, sys, socket, time
from random import randint

# Bases for generators of up to 29:
# 2, 3, 8, 10, 11, 14, 15, 18, 19, 21, 26, 27
# Up to 23:
# 5, 7, 10, 11, 14, 15, 17, 19, 20, 21,
def get_offset(n, base=19):
	return base**n % base

# returns an 'n' sized string to be appened to plaintext
def pad(n):
	return [chr(randint(0,28)+97) for x in xrange(n)]
	# return "".join()

# TBD
def scramble(text, key, offset):
	pass


# 	Crypto part:
# 		Encryption:
# 			Message is padded up to a certain number of characters (max length) with random text
# 			You create a one time AES key
# 			You encrypt the Message using AES and the above key
# 			You create a random character (a-z, {|}~) that maps to 0-28 via ord([actual char]) - 97
# 			You pass the random character thru one of the base generators for 29 (below) that return the step/increment value
# 			You scramble the Key within the text in gaps of getoffset(randchar)
# 			randchar goes in the front of the ciphertext
def encrypt(message):
	# messagee is turned into a list
	plaintext = message.split()

	# Add Random Padding
	plaintext.extend(pad(set_size-len(plaintext)))
	# this turns plaintext into a string
	plaintext = "".join(plaintext)

	# everything below doesn't work yet, just a placeholder
	key = AES.generate_key(128)
	# Scrambled Eggs Time
	plaintext = scramble(plaintext, key, offset)
	output = AES.encrypt(cyphertext, key)
	return output

# Decrypt:
# Delete first char, and pass it thru getoffset. Use result to build key and message
# AES Decrypt
def decrypt(message):
	# if the message received it's not the specific size/length, return and print nothing
	if len(message) != size:
		return ""
	# IS IT QUARANTEED THAT THIS WILL HAPPEN ALL THE TIME?
	# NEED TO TEST AES RETURN SIZE GIVEN MOST INPUTS

	# DO THE THING
	random_char = ord(message[0] - 97)
	offset = getoffset(random_char)
	# skipping the random_char
	ciphertext = message[1:] 

	# Unscramble, not done
	for index in xrange(len(message)-32):
		pass

	# this doesn't work yet, just a placeholder
	output = AES.decrypt(cyphertext, key)
	return output

# Client code talking to server:
# https://neerajkhandelwal.wordpress.com/2012/02/16/socket-programming-handling-multiclients/

def main():
	pass

if __name__ == '__main__':
	main()