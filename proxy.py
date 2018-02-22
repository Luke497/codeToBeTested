import os,sys,thread
from socket import * 

BACKLOG = 50            # how many pending connections queue will hold
MAX_DATA_RECV = 4096    # max number of bytes we receive at once
DEBUG = True           # set to True to see the debug msgs

def handleRequest(conn):
`   # get the request from browser
      request = conn.recv(MAX_DATA_RECV)
      # parse the first line
      first_line = request.split('n')[0]

      # get url
      url = first_line.split(' ')[1]

      # find the webserver and port
      http_pos = url.find("://")          # find pos of ://
      if (http_pos==-1):
        temp = url
      else:
        temp = url[(http_pos+3):]       # get the rest of url

      port_pos = temp.find(":")           # find the port pos (if any)

      # find end of web server
      webserver_pos = temp.find("/")
      if webserver_pos == -1:
        webserver_pos = len(temp)

      webserver = ""
      port = -1
      if (port_pos==-1 or webserver_pos < port_pos):      # default port
        port = 80
        webserver = temp[:webserver_pos]
      else:       # specific port
        port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
        webserver = temp[:port_pos]

      print "Connect to:", webserver, port

      try:
        # create a socket to connect to the web server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((webserver, port))
        s.send(request)         # send request to webserver

        while 1:
          # receive data from web server
          data = s.recv(MAX_DATA_RECV)

          if (len(data) > 0):
            # send to browser
            conn.send(data)
          else:
            break
        s.close()
        conn.close()
      except socket.error, (value, message):
        if s:
          s.close()
        if conn:
          conn.close()
        print "Runtime Error:", message
        sys.exit(1)

def startServer(serverAddress, serverPort):
        # 1. Create server socket
        serverSocket = socket(AF_INET, SOCK_STREAM)
        # 2. Bind the server socket to server address and server port
        serverSocket.bind((serverAddress,serverPort))
        # 3. Continuously listen for connections to server socket
        serverSocket.listen(BACKLOG)
        try:
                while True:
                # 4. When a connection is accepted, call handleRequest function, passing new connection socket (see https://docs.python.org/2/library/socket.html#socket.socket.accept)
                        connectionSocket, addr = serverSocket.accept()
                        start_new_thread(handleRequest(connectionSocket,addr))
        except KeyboardInterrupt:
        #5. Close server socket
                serverSocket.close()

startServer("", 91)
