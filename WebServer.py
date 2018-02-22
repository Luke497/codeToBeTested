#!/usr/bin/python
# -*- coding: UTF-8 -*-

from socket import * 
import sys 
from thread import *

def handleRequest(tcpSocket):
        # 1. Receive request message from the client on connection socket
        message = tcpSocket.recv(1024)
        # 2. Extract the path of the requested object from the message (second part of the HTTP header)
        filename = message.split()[1]
        try:
                
                # 3. Read the corresponding file from disk
                # 4. Store in temporary buffer
                f = open(filename[1:])        
        except:
                f = open('error.html')
        outputdata = f.read()
        # 5. Send the correct HTTP response error
        tcpSocket.send('HTTP/1.0 200 OK\r\n\r\n')
        # 6. Send the content of the file to the socket
        tcpSocket.sendall(outputdata)
        tcpSocket.close()

def startServer(serverAddress, serverPort):
        # 1. Create server socket
        serverSocket = socket(AF_INET, SOCK_STREAM)
        # 2. Bind the server socket to server address and server port
        serverSocket.bind((serverAddress, serverPort))
        # 3. Continuously listen for connections to server socket
        serverSocket.listen(1)
        try:
                while True:
                # 4. When a connection is accepted, call handleRequest function, passing new connection socket (see https://docs.python.org/2/library/socket.html#socket.socket.accept)
                        connectionSocket, addr = serverSocket.accept()
                        start_new_thread(handleRequest(connectionSocket))
        except KeyboardInterrupt:
        # 5. Close server socket
                serverSocket.close()

try:
        port = input("What port? (Leave empty for default) ")
except SyntaxError:
        port = 999
startServer("", port)
