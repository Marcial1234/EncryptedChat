# EncryptedChat
Introduction to Cryptology - CIS 4362 Project

Once the repo is cloned all one has to do is run the server in the command line by cd’ing into the folder “EncryptedChat” and running “python server.py”. Once the server is running you can run the client without any encryption by running “python clientNoCrypto.py”. This will show that the server receives all messages from that client in plain text. To run the app’s client, first download and install the crypto library from https://pypi.python.org/pypi/pycrypto. Then run “python client.py”. This will show that any message sent to the server will be encrypted and thus if anyone is attacking the server or sniffing the network, they will only get ciphertext. The server does not do any of the encryption, it is all done client side.
