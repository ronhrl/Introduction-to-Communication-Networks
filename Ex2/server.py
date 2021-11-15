import socket
import string
import sys
import os
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = int(sys.argv[1])
server.bind(('', port))

server.listen(5)
while True:
    client_socket, client_address = server.accept()
    data = client_socket.recv(100)
    if data[0] == "path":
        # To add a link
        rand_id = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=128))
        client_socket.send(rand_id)
# while True:
#     client_socket, client_address = server.accept()
#     print('Connection from: ', client_address)
#     data = client_socket.recv(100)
#     print('Received: ', data)
#     client_socket.send(data.upper())
#     data = client_socket.recv(100)
#     print('Received: ', data)
#     client_socket.send(data.upper())
#     client_socket.close()
#    print('Client disconnected')
