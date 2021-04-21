import socket
import message_pb2

# UDP Stuff
IP = "127.0.0.1"
PORT = 5005
BUFFER = 1024

serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
serverSock.bind((IP, PORT))

while True:

    print("Server running and listening ... ")

    data, addr = serverSock.recvfrom(BUFFER)

    print(data)
    print(addr)

    message = message_pb2.Status()
    message.ParseFromString(data)
    
    print(f"GOT {message}")
