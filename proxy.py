import os,sys,thread
from socket import * 

BACKLOG = 50            # how many pending connections queue will hold
MAX_DATA_RECV = 4096    # max number of bytes we receive at once
DEBUG = True           # set to True to see the debug msgs

def handleRequest(s):
    # create a thread to handle request
    thread.start_new_thread(proxy_thread, (conn, client_addr))

def startServer(serverAddress, serverPort):
        # 1. Create server socket
        serverSocket = socket(AF_INET, SOCK_STREAM)
        # 2. Bind the server socket to server address and server port
        serverSocket.bind((serverAddress, serverPort))
        # 3. Continuously listen for connections to server socket
        serverSocket.listen(BACKLOG)
        try:
                while True:
                # 4. When a connection is accepted, call handleRequest function, passing new connection socket (see https://docs.python.org/2/library/socket.html#socket.socket.accept)
                        connectionSocket, addr = serverSocket.accept()
                        start_new_thread(handleRequest(connectionSocket))
        except KeyboardInterrupt:
        # 5. Close server socket
                serverSocket.close()

startServer("", 90)
