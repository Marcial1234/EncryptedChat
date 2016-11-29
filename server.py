# !/usr/bin/python
# test this line if you're in Mac/Linux

import os, sys, socket, time
from uuid import getnode as get_mac
# function for MAC address

# pycrypto Package
# from Crypto.Cipher import AES
# I'm having issues having issues installing the AES package in UF's computers
# trying alternatives, like M2Crypto or open sourced vanilla AES implementations

HOST = ''    # All available interfaces
PORT = 52725 # Arbitrary port

# Function for handling connections. This will be used to create threads
def clientthread(client):
    # Sending message to connected client
    client.send('Welcome to the server. Type something and hit enter\n') # send only takes string
    
    # infinite loop so that function do not terminate and thread do not end.
    while True:
        
        # Receiving from client
        data = client.recv(1024)
        reply = 'OK...' + data
        if not data: 
            break
     
        client.sendall(reply)
    
    client.close()

def main():
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print 'Socket created'
	 
	# Bind socket to local host and port
	server.bind((HOST, PORT))

	# Debug Code
	# try:
	#     server.bind((HOST, PORT))
	# except socket.error as msg:
	#     print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	#     syserver.exit()

	print 'Socket bind complete'

	# Start listening on socket
	# Passed Parameter is # of max connections allowed
	server.listen(4)
	print 'Socket now listening'

	basic_key = get_mac()

	# Stay Connected undefinately
	# TODO: How to kill it??
	while True:
	    # wait to accept a connection - BLOCKING call
	    client, (ip,port) = server.accept()
	    start_new_thread(clientthread, (client,))
	    print 'Connected with ' + ip + ':' + str(port)

	    addr = str(basic_key)
	    # this list comp formats the MAC Address from a Long to "XX:XX:.."
	    addr = ':'.join(addr[i:i+2] for i in range(0,12,2))
	    # send server mac address to client as a test
	    client.send(addr)

	    # time.sleep(10)
	    # exits after one, still figuring out to how gracefully exit
	    break

	server.close()

if __name__ == '__main__':
	main()